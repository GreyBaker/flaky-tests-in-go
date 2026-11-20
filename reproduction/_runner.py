import argparse
import hashlib
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import tempfile
import time
import uuid

DEFAULT_RUNS = 500
DEFAULT_SECONDS = 3600
MAX_CLEANUP_SECONDS = 10
CLEANUP_BUDGET_FRACTION = 0.1
WINDOWS_KILL_TIMEOUT_SECONDS = 5
BUILD_JOBS = 2
DEFAULT_BATCH = 1
DEFAULT_CPUS = 4
DEFAULT_MEMORY = "6g"
DEFAULT_GO_THREADS = 4
DEFAULT_TEST_PARALLELISM = 4
DEFAULT_TEST_TIMEOUT = "10m"
UNPRIVILEGED_USER = "65534:65534"
CONTAINER_PID_LIMIT = 2048
SCRATCH_RAM_SIZE = "2g"
TMP_RAM_SIZE = "512m"
SCRATCH_MODE = "1777"
TIME_LIMIT_EXIT = 124
INTERRUPTED_EXIT = 130
RUNNER_ERROR_EXIT = 2
SUBJECT_EXIT_CODES = {0, 1, 2, 66}

# Pinned toolchain and etcd dependency for container builds.
GO = "golang:1.26.3-bookworm@sha256:386d475a660466863d9f8c766fec64d7fdad3edac2c6a05020c09534d71edb4b"
ETCD = """RUN curl -fL https://github.com/etcd-io/etcd/releases/download/v3.7.1/etcd-v3.7.1-linux-amd64.tar.gz -o /tmp/etcd.tgz \\
 && echo 'e8cd3fa8064c98137c5dbd78b76f969417ace84efb83c481041d7a52ffdd8fb9  /tmp/etcd.tgz' | sha256sum -c - \\
 && mkdir /opt/etcd && tar -xzf /tmp/etcd.tgz --strip-components=1 -C /opt/etcd \\
 && cp /opt/etcd/etcd /usr/local/bin/etcd"""


# Internal stop signal, handled separately from subject failures.
class Limit(Exception):
    pass


# Share runner options and a monotonic clock across setup and execution.
class Clock:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--runs", type=int, default=DEFAULT_RUNS)
        parser.add_argument("--seconds", type=float, default=DEFAULT_SECONDS)
        self.args = parser.parse_args()
        if self.args.runs < 1 or not 0 < self.args.seconds < float("inf"):
            parser.error("Both limits must be positive and finite.")
        self.end = time.monotonic() + self.args.seconds
        self.reserve = min(MAX_CLEANUP_SECONDS, self.args.seconds * CLEANUP_BUDGET_FRACTION)

    def left(self, cleanup=False):
        left = self.end - time.monotonic() - (0 if cleanup else self.reserve)
        if left <= 0:
            raise Limit()
        return left

    def call(self, argv, *, capture=False, cleanup=False, **kwargs):
        limit = self.left(cleanup)
        # Stream output unless the caller needs to inspect the result.
        process = subprocess.Popen(
            argv, stdout=subprocess.PIPE if capture else None, stderr=subprocess.STDOUT,
            start_new_session=os.name != "nt", **kwargs)
        try:
            output, _ = process.communicate(timeout=limit)
            return process.returncode, output.decode("utf-8", errors="replace").strip() if output else ""
        except BaseException:
            # Stop the child process tree before propagating an interruption.
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               timeout=WINDOWS_KILL_TIMEOUT_SECONDS)
            else:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            process.wait()
            raise

    def checked(self, argv, **kwargs):
        # Setup failures are runner errors, not flaky-test observations.
        code, output = self.call(argv, **kwargs)
        if code:
            raise RuntimeError(f"Setup exited {code}: {output or shlex.join(map(str, argv))}")
        return output


def finish(function):
    # Keep interruption and setup errors distinct from subject failures.
    try:
        return function()
    except (Limit, subprocess.TimeoutExpired):
        print("\nTime limit reached; this is not a test failure.", flush=True)
        return TIME_LIMIT_EXIT
    except KeyboardInterrupt:
        print("\nStopped.", flush=True)
        return INTERRUPTED_EXIT
    except (OSError, RuntimeError) as error:
        print(f"\nSetup/runner error: {error}", file=sys.stderr, flush=True)
        return RUNNER_ERROR_EXIT


def container(file, command, *, recipe=None, batch=DEFAULT_BATCH,
              cpus=DEFAULT_CPUS, memory=DEFAULT_MEMORY,
              gomax=DEFAULT_GO_THREADS, user=UNPRIVILEGED_USER, network="none", writable=False,
              options=(), status="", step=1, tmpfs_tmp=True, scratch="memory"):
    def run():
        clock = Clock()
        directory = Path(file).resolve().parent
        print(f"{directory.name} [recorded: {status}]", flush=True)
        if clock.args.runs < step:
            raise RuntimeError(f"This workload needs at least {step} repetitions per batch.")
        # Build from case-local files, without a historical replication checkout.
        with tempfile.TemporaryDirectory(prefix="presented-build-") as temporary:
            context = Path(temporary)
            dockerfile = recipe if recipe is not None else (directory / "Dockerfile").read_text()
            dockerfile += f"\nRUN mkdir -p /scratch && chmod {SCRATCH_MODE} /scratch\n"
            (context / "Dockerfile").write_text(dockerfile, encoding="utf-8", newline="\n")
            # Cache images by their recipe and local build inputs.
            fingerprint = hashlib.sha256(dockerfile.encode())
            for source in sorted(directory.iterdir()):
                if source.is_file() and source.name not in ["run.py", "Dockerfile"]:
                    data = source.read_bytes()
                    (context / source.name).write_bytes(data)
                    fingerprint.update(source.name.encode() + data)
            image = "presented-replication:" + fingerprint.hexdigest()
            code, _ = clock.call(["docker", "image", "inspect", image], capture=True)
            if code:
                clock.checked(["docker", "build", "--platform=linux/amd64", "-t", image, str(context)])
        requested, failed = 0, False
        while requested + step <= clock.args.runs:
            clock.left()
            count = min(batch, clock.args.runs - requested)
            count -= count % step
            name = "presented-" + uuid.uuid4().hex
            created = False
            try:
                # Give each batch its own container and writable scratch space.
                argv = ["docker", "create", "--name", name, "--init", "--platform=linux/amd64",
                        "--cpus", str(cpus), "--memory", memory,
                        "--pids-limit", str(CONTAINER_PID_LIMIT),
                        "--network", network, "--cap-drop", "ALL",
                        "--security-opt", "no-new-privileges", "--user", user,
                        *(["--mount", "type=volume,target=/scratch"] if scratch == "disk" else
                          ["--tmpfs", f"/scratch:rw,nosuid,nodev,size={SCRATCH_RAM_SIZE},mode={SCRATCH_MODE}"]),
                        *(["--tmpfs", f"/tmp:rw,nosuid,nodev,size={TMP_RAM_SIZE},mode={SCRATCH_MODE}"] if tmpfs_tmp else []),
                        "-e", f"COUNT={count}", "-e", f"GOMAXPROCS={gomax}",
                        "-e", "HOME=/scratch", "-e", "TMPDIR=/scratch",
                        *([] if writable else ["--read-only"]), *options,
                        "--entrypoint", "bash", image, "-c", command]
                clock.checked(argv, capture=True)
                created = True
                requested += count
                print(f"\n--- requested {requested}/{clock.args.runs} ---", flush=True)
                code, _ = clock.call(["docker", "start", "-a", name])
                oom = clock.checked(["docker", "inspect", "-f", "{{.State.OOMKilled}}", name], capture=True)
                print(f"Process exit: {code}", flush=True)
                failed |= code != 0
                if oom == "true":
                    # An OOM is an environment failure, not a reproduced flake.
                    raise RuntimeError("Container ran out of memory.")
                if code not in SUBJECT_EXIT_CODES:
                    raise RuntimeError(f"Container/subject stopped with exit {code}; inspect output above.")
            finally:
                # Remove only this invocation's container and anonymous volumes.
                code, output = clock.call(["docker", "rm", "-f", "-v", name], capture=True, cleanup=True)
                if code:
                    print(f"Cleanup needs attention: {name}: {output}", file=sys.stderr)
                    if created:
                        raise RuntimeError(f"Could not remove owned container {name}.")
        return int(failed)
    raise SystemExit(finish(run))


def go(file, repository, revision, package, selector, *, image=GO, flags="",
       goflags="-mod=readonly", module="", source="/src", prepare="", build="",
       before="", timeout=DEFAULT_TEST_TIMEOUT, test_flags="", batch=DEFAULT_BATCH,
       cpus=DEFAULT_CPUS, memory=DEFAULT_MEMORY,
       gomax=DEFAULT_GO_THREADS, user=UNPRIVILEGED_USER, options=(), status="", network="none",
       writable=False, step=1, command=None, etcd=False, scratch="memory"):
    work = source + ("/" + module if module else "")
    # Fetch pinned upstream source and compile its unchanged test package.
    recipe = f"""# syntax=docker/dockerfile:1
FROM {image}
SHELL ["/bin/bash", "-c"]
ENV GOTOOLCHAIN=local GOENV=off GOFLAGS={shlex.quote(goflags)} GOMAXPROCS={BUILD_JOBS}
RUN git init {source} && git -C {source} remote add origin https://github.com/{repository}.git \\
 && git -C {source} fetch --depth=1 origin {revision} && git -C {source} checkout --detach FETCH_HEAD
WORKDIR {work}
{ETCD if etcd else ''}
{prepare}
RUN --mount=type=cache,target=/root/.cache/go-build \\
 --mount=type=cache,target=/go/pkg/mod \\
 {build or f'go test -c -p={BUILD_JOBS} {flags} -o /opt/test {package}'}
"""
    directory = package.removeprefix("./")
    # Run beside the upstream fixtures, as go test normally would.
    cwd = work + ("/" + directory if package.startswith("./") and directory != "." else "")
    test = f"/opt/test -test.v -test.count=\"$COUNT\" -test.parallel={DEFAULT_TEST_PARALLELISM} -test.timeout={timeout} -test.run={shlex.quote(selector)} {test_flags}"
    # Special workloads can wrap the same compiled-test command with peers.
    body = (f"cd {shlex.quote(cwd)}\n" + command.replace("{test}", test)) if command else f"set -e\ncd {shlex.quote(cwd)}\n{before}\nexec {test}"
    container(file, body, recipe=recipe, batch=batch, cpus=cpus, memory=memory,
              gomax=gomax, user=user, options=options, status=status,
              network=network, writable=writable, step=step, scratch=scratch)


def native_go(file, repository, revision, package, selector, *, platform=None,
              version="go1.26.3", flags="", timeout=DEFAULT_TEST_TIMEOUT, batch=DEFAULT_BATCH, module="",
              env=None, requires=(), setup=(), toolchain_source=False, test_flags=(),
              private_docker=False, bin_dirs=(), status=""):
    def run():
        clock = Clock()
        print(f"{Path(file).resolve().parent.name} [recorded: {status}]", flush=True)
        # Native cases need their reported platform and real external services.
        if platform and not (sys.platform == platform or
                             platform == "openbsd" and sys.platform.startswith("openbsd")):
            raise RuntimeError(f"Run on {platform}, not {sys.platform}.")
        for name in requires:
            if not os.environ.get(name):
                raise RuntimeError(f"Set {name} for the real test environment first.")
        if private_docker:
            # Refuse the normal host Docker socket for integration tests.
            endpoint = os.environ.get("DOCKER_HOST", "")
            socket = Path(endpoint.removeprefix("unix://")).resolve()
            if not endpoint.startswith("unix://") or socket in [
                    Path("/var/run/docker.sock").resolve(), Path("/run/docker.sock").resolve()]:
                raise RuntimeError("Set DOCKER_HOST to a disposable, private Unix-socket daemon.")
        # Reuse a private checkout, but leave edits or mismatched revisions intact.
        cache = Path(tempfile.gettempdir()) / "opencode/presented-replication" / repository / revision
        source = cache / "source"
        cache.mkdir(parents=True, exist_ok=True)
        if not (source / ".git").is_dir():
            source.mkdir(exist_ok=True)
            clock.checked(["git", "init", str(source)])
            clock.checked(["git", "-C", str(source), "-c", "core.autocrlf=false",
                           "fetch", "--depth=1", f"https://github.com/{repository}.git", revision])
            clock.checked(["git", "-C", str(source), "-c", "core.autocrlf=false",
                           "checkout", "--detach", "FETCH_HEAD"])
        if clock.checked(["git", "-C", str(source), "rev-parse", "HEAD"], capture=True) != revision:
            raise RuntimeError("Cached checkout has a different revision; leave it intact and inspect it.")
        if clock.checked(["git", "-C", str(source), "status", "--porcelain"], capture=True):
            raise RuntimeError("Cached source was edited; leave it intact and inspect it.")
        environment = dict(os.environ, GOENV="off", GOTOOLCHAIN=version, GOMAXPROCS=str(DEFAULT_GO_THREADS),
                           CGO_ENABLED="0", GOFLAGS="-mod=readonly")
        environment.update(env or {})
        for relative in bin_dirs:
            (source / relative).mkdir(parents=True, exist_ok=True)
        if bin_dirs:
            environment["PATH"] = os.pathsep.join(str(source / relative) for relative in bin_dirs) + os.pathsep + environment["PATH"]
        go_binary = "go"
        if toolchain_source:
            # Go-runtime cases build and use the selected upstream toolchain.
            bootstrap = clock.checked(["go", "env", "GOROOT"], capture=True)
            environment.update(GOROOT_BOOTSTRAP=bootstrap, GOTOOLCHAIN="local", CGO_ENABLED="1", GOFLAGS="")
            clock.checked(["bash", "make.bash"], cwd=source / "src", env=environment)
            go_binary = str(source / "bin/go")
            environment["GOROOT"] = str(source)
        cwd = source / module
        for command in setup:
            clock.checked(command, cwd=cwd, env=environment)
        # Compile once, then execute from the package's fixture directory.
        binary = cache / ("test.exe" if os.name == "nt" else "test")
        clock.checked([go_binary, "test", "-c", f"-p={BUILD_JOBS}", *shlex.split(flags),
                       "-o", str(binary), package], cwd=cwd, env=environment)
        requested, failed = 0, False
        test_cwd = (source / "src" / package) if toolchain_source else (
            cwd / package.removeprefix("./") if package.startswith("./") else cwd)
        while requested < clock.args.runs:
            count = min(batch, clock.args.runs - requested)
            requested += count
            print(f"\n--- requested {requested}/{clock.args.runs} ---", flush=True)
            code, _ = clock.call([str(binary), "-test.v", f"-test.count={count}",
                                  f"-test.timeout={timeout}", f"-test.run={selector}", *test_flags],
                                 cwd=test_cwd, env=environment)
            print(f"Process exit: {code}", flush=True)
            failed |= code != 0
            if code not in SUBJECT_EXIT_CODES:
                break
        return int(failed)
    raise SystemExit(finish(run))

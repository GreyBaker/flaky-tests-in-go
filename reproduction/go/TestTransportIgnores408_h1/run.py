import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import container

RUNS_PER_PROCESS = 1000
GO_PROCESS_DEADLINE = '120s'
PACKAGE_JOBS = 4
SHUFFLE_SEED = 42

if __name__ == "__main__":
    container(__file__,
        command=f"""\
export GOPATH=/scratch/gopath GOCACHE=/scratch/cache
exec go test -v -count="$COUNT" -timeout={GO_PROCESS_DEADLINE} -p={PACKAGE_JOBS} -short -shuffle={SHUFFLE_SEED} -run="^TestTransport(Ignores408|ProxyDialDoesNotMutateProxyConnectHeader)$" net/http
""",
        batch=RUNS_PER_PROCESS,
        writable=True,
        network='bridge',
        status='verified',
    )

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 10
CPU_QUOTA = 1
PINNED_CPU = '0'

if __name__ == "__main__":
    go(__file__,
        repository='syncthing/syncthing',
        revision='fa40ccece1da3925ce6db890aec295ffc311a1d4',
        package='./lib/model',
        selector='^TestRecvOnlyRemoteUndoChanges$',
        image='golang:1.15.15-buster@sha256:414340e7bfee1b13c72c59e9b0df5488b83b6a5c99c2d806509304ca7ef71350',
        batch=RUNS_PER_PROCESS,
        cpus=CPU_QUOTA,
        options=['--cpuset-cpus', PINNED_CPU],
        command="""\
yes >/dev/null & a=$!
yes >/dev/null & b=$!
{test}
code=$?
kill "$a" "$b" 2>/dev/null || true
wait 2>/dev/null || true
exit "$code"
""",
        status='verified',
    )

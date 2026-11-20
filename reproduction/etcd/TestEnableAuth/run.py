import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

WORKERS_PER_PAIR = 2
RUNS_PER_WORKER = 1

if __name__ == "__main__":
    go(__file__,
        repository='etcd-io/etcd',
        revision='7ee95a61a02ceea4ca7400342f75fdab7677943b',
        package='./server/embed',
        selector='^TestEnableAuth$',
        batch=WORKERS_PER_PAIR,
        step=WORKERS_PER_PAIR,
        command=f"""\
COUNT={RUNS_PER_WORKER}
mkdir -p /scratch/a /scratch/b
(cd /scratch/a; {{test}}) & a=$!
(cd /scratch/b; {{test}}) & b=$!
wait "$a"; first=$?
wait "$b"; second=$?
if ((first || second)); then exit 1; fi
""",
        status='verified',
    )

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

GO_PROCESS_DEADLINE = '180s'
PAUSE_AFTER_SECONDS = 18
PAUSE_DURATION_SECONDS = 8

if __name__ == "__main__":
    go(__file__,
        repository='moby/moby',
        revision='7c2d5175eec0dea354b65da66c0fe7c46610712d',
        package='./daemon/libnetwork/networkdb',
        selector='^TestNetworkDBGarbageCollection$',
        goflags='-mod=vendor',
        prepare='ENV CGO_ENABLED=0',
        timeout=GO_PROCESS_DEADLINE,
        command=f"""\
{{test}} & subject=$!
(sleep {PAUSE_AFTER_SECONDS}; kill -STOP "$subject"; sleep {PAUSE_DURATION_SECONDS}; kill -CONT "$subject") & timer=$!
wait "$subject"; code=$?
kill "$timer" 2>/dev/null || true
wait "$timer" 2>/dev/null || true
exit "$code"
""",
        status='verified',
    )

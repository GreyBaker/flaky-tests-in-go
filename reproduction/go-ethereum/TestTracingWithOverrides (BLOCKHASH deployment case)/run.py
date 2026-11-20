import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 1000
GO_PROCESS_DEADLINE = '45m'

if __name__ == "__main__":
    go(__file__,
        repository='ethereum/go-ethereum',
        revision='b20778d77d50e2c9775cb4d2fa872579989c5421',
        package='./eth/tracers',
        selector='^TestTracingWithOverrides$',
        batch=RUNS_PER_PROCESS,
        timeout=GO_PROCESS_DEADLINE,
        status='verified',
    )

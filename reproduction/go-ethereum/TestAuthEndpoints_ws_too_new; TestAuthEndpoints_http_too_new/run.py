import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 1000
GO_PROCESS_DEADLINE = '45m'

if __name__ == "__main__":
    go(__file__,
        repository='ethereum/go-ethereum',
        revision='0ef7a39e78e37d6df6898fe507e0b3b6851dbd25',
        package='./node',
        selector='^TestAuthEndpoints$',
        batch=RUNS_PER_PROCESS,
        timeout=GO_PROCESS_DEADLINE,
        status='verified',
    )

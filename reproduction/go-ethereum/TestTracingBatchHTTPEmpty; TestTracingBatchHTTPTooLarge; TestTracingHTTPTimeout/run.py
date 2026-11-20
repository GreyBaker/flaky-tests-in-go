import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 100
GO_PROCESS_DEADLINE = '45m'

if __name__ == "__main__":
    go(__file__,
        repository='ethereum/go-ethereum',
        revision='38667bc64eb568bdb1632fe9134d189adf3cefe9',
        package='./rpc',
        selector='^TestTracing(BatchHTTPEmpty|BatchHTTPTooLarge|HTTPTimeout)$',
        batch=RUNS_PER_PROCESS,
        timeout=GO_PROCESS_DEADLINE,
        status='verified',
    )

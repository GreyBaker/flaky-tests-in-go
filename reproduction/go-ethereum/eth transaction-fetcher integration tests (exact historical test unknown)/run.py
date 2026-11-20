import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

CPU_QUOTA = 1
MEMORY_LIMIT = '1g'
GO_PROCESS_DEADLINE = '45m'

if __name__ == "__main__":
    go(__file__,
        repository='ethereum/go-ethereum',
        revision='ce64ab44ed5209e7ac9c9ac5af383309483d155b',
        package='./eth',
        selector='^TestRecvTransactions69$',
        cpus=CPU_QUOTA,
        memory=MEMORY_LIMIT,
        options=['--memory-swap', MEMORY_LIMIT],
        timeout=GO_PROCESS_DEADLINE,
        status='unverified',
    )

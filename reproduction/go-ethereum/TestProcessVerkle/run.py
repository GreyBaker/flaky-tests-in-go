import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

CPU_QUOTA = 0.5
MEMORY_LIMIT = '1g'
GO_PROCESS_DEADLINE = '45m'

if __name__ == "__main__":
    go(__file__,
        repository='ethereum/go-ethereum',
        revision='3f1871524fda4e8da31fbbad927e554993228575',
        package='./core',
        selector='^TestProcessVerkle$',
        cpus=CPU_QUOTA,
        memory=MEMORY_LIMIT,
        options=['--memory-swap', MEMORY_LIMIT],
        timeout=GO_PROCESS_DEADLINE,
        scratch='disk',
        status='verified',
    )

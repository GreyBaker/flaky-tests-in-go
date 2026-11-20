import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

CPU_QUOTA = 1
MEMORY_LIMIT = '1g'

if __name__ == "__main__":
    go(__file__,
        repository='prometheus/prometheus',
        revision='68119c094875452839d34d259b7394d0176cb844',
        package='./cmd/prometheus',
        selector='^TestHeadCompactionWhileScraping$',
        flags='-race',
        cpus=CPU_QUOTA,
        memory=MEMORY_LIMIT,
        options=['--memory-swap', MEMORY_LIMIT],
        status='unverified',
    )

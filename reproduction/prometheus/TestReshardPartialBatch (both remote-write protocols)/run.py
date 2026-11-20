import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

CPU_QUOTA = 1
MEMORY_LIMIT = '1g'

if __name__ == "__main__":
    go(__file__,
        repository='prometheus/prometheus',
        revision='2aefd00c24fbc316d362cf7e6b62fd0021f168ae',
        package='./storage/remote',
        selector='^TestReshardPartialBatch$',
        flags='-race',
        cpus=CPU_QUOTA,
        memory=MEMORY_LIMIT,
        options=['--memory-swap', MEMORY_LIMIT],
        status='unverified',
    )

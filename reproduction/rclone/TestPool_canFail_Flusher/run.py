import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

CPU_QUOTA = 1
MEMORY_LIMIT = '1g'

if __name__ == "__main__":
    go(__file__,
        repository='rclone/rclone',
        revision='cce399515fbe58d91584b932218e5aaf899eb661',
        package='./lib/pool',
        selector='^TestPool$/^canFail$/^Flusher$',
        cpus=CPU_QUOTA,
        memory=MEMORY_LIMIT,
        options=['--memory-swap', MEMORY_LIMIT],
        scratch='disk',
        status='unverified',
    )

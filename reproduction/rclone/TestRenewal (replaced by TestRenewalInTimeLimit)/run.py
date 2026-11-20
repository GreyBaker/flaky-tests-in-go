import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 1000
MEMORY_LIMIT = '4g'

if __name__ == "__main__":
    go(__file__,
        repository='rclone/rclone',
        revision='23d17b76bef82cc88e382128949d4e583bf9ea39',
        package='./backend/seafile',
        selector='^TestRenewal$',
        flags='-race',
        batch=RUNS_PER_PROCESS,
        memory=MEMORY_LIMIT,
        status='verified',
    )

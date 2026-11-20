import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 100

if __name__ == "__main__":
    go(__file__,
        repository='rclone/rclone',
        revision='e906ecf25f0f521d644a40de74c7fd46c123b3ec',
        package='./lib/transform',
        selector='^TestVarious$',
        batch=RUNS_PER_PROCESS,
        status='unverified',
    )

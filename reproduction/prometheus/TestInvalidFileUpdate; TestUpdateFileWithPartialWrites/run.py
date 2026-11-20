import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 100

if __name__ == "__main__":
    go(__file__,
        repository='prometheus/prometheus',
        revision='05f9eb8b3b8e10b48c8f4153b0714dbe9bc9a630',
        package='./discovery/file',
        selector='^Test(InvalidFileUpdate|UpdateFileWithPartialWrites)$',
        batch=RUNS_PER_PROCESS,
        status='unverified',
    )

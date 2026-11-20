import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 100

if __name__ == "__main__":
    go(__file__,
        repository='prometheus/prometheus',
        revision='3aba7dca59310df83997c27a75b4f1343ba68cde',
        package='./tsdb',
        selector='^TestQuerierShouldNotFailIfOOOCompactionOccursAfter',
        batch=RUNS_PER_PROCESS,
        status='unverified',
    )

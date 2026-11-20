import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 100

if __name__ == "__main__":
    go(__file__,
        repository='prometheus/prometheus',
        revision='0f5727f420f890d9bb5679325a2d606a9da7ac23',
        package='./tsdb',
        selector='^TestCancelCompactions$',
        batch=RUNS_PER_PROCESS,
        status='unverified',
    )

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 50
CPU_QUOTA = 1
GO_THREADS = 1

if __name__ == "__main__":
    go(__file__,
        repository='ollama/ollama',
        revision='2c73164246534c57acfdb37cc96b39eccf4ccc81',
        package='./server',
        selector='^TestGGUFMetadataNotPublishedAfterDelete$',
        batch=RUNS_PER_PROCESS,
        cpus=CPU_QUOTA,
        gomax=GO_THREADS,
        status='verified',
    )

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 100

if __name__ == "__main__":
    go(__file__,
        repository='ollama/ollama',
        revision='e51dead6363e941b480f5bf1270254db7e175083',
        package='./model/renderers',
        selector='^TestOlmo3Renderer$',
        batch=RUNS_PER_PROCESS,
        status='verified',
    )

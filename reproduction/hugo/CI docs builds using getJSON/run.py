import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import container

if __name__ == "__main__":
    container(__file__,
        command='exec /opt/hugo --source /src/docs --destination /scratch/site',
        network='bridge',
        writable=True,
        status='unverified',
    )

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import native_go

if __name__ == "__main__":
    native_go(__file__,
        repository='ollama/ollama',
        revision='83d4311ffecb79bf3a7a1f0341afa4eb069da853',
        package='./x/transfer',
        selector='^TestDownloadParallelism$',
        platform='win32',
        env={},
        status='unverified',
    )

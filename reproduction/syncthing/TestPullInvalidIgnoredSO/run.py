import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

if __name__ == "__main__":
    go(__file__,
        repository='syncthing/syncthing',
        revision='1df8701c46e993e80bd79d7751766ae543149742',
        package='./lib/model',
        image='golang:1.12.17-buster@sha256:d9d06cb747d49db5d5703610ecdef837c0432efcaccc4a5959155dd61fe42f4a',
        selector='^TestPullInvalidIgnoredSO$',
        status='unverified',
    )

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

if __name__ == "__main__":
    go(__file__,
        repository='go-gitea/gitea',
        revision='5badd1bdeef0e22bc6d001c763a5baf506156298',
        package='./models/issues',
        selector='^TestResourceIndex$',
        flags='-race',
        prepare='RUN apt-get update && apt-get install -y --no-install-recommends git-lfs',
        status='unverified',
    )

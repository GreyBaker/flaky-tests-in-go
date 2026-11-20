import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

if __name__ == "__main__":
    go(__file__,
        repository='etcd-io/etcd',
        revision='cf3527b67ed7bac557ed023af91821792abeaaf7',
        package='./tests/common',
        selector='^TestKVGet$',
        flags='-tags=integration',
        status='unverified',
    )

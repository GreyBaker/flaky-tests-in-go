import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

if __name__ == "__main__":
    go(__file__,
        repository='etcd-io/etcd',
        revision='5791f2b80ecfcae792fd196d2c25f51123ea3d07',
        package='./tests/integration',
        selector='^TestV3AuthNestedTxnPermissionDenied$',
        flags='-tags=integration',
        status='unverified',
    )

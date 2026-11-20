import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import native_go

if __name__ == "__main__":
    native_go(__file__,
        repository='usememos/memos',
        revision='00f21b86e2110c10388eee14b4b0ab85db6bfcc6',
        package='./store/test',
        selector='^TestMigration',
        platform='linux',
        private_docker=True,
        env={'CGO_ENABLED': '1'},
        status='unverified',
    )

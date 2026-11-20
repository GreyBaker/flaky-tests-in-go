import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import native_go

if __name__ == "__main__":
    native_go(__file__,
        repository='syncthing/syncthing',
        revision='22e133cce697abc58b9570e2587b69ceae0fcdef',
        package='./lib/fs',
        selector='^TestWatchIgnore$',
        platform='openbsd',
        version='local',
        env={'GO111MODULE': 'on', 'GOFLAGS': '-mod=readonly'},
        status='unverified',
    )

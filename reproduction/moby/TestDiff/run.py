import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import native_go

if __name__ == "__main__":
    native_go(__file__,
        repository='moby/moby',
        revision='c0e36f699a9a7cb6a2e1ccd78756e17440c6a3f1',
        package='./integration/container',
        selector='^TestDiff$',
        platform='linux',
        env={'GOFLAGS': '-mod=vendor', 'CGO_ENABLED': '1'},
        private_docker=True,
        requires=['DOCKER_INTEGRATION_DAEMON_DEST'],
        bin_dirs=['bundles/binary-daemon'],
        setup=[['go', 'build', '-o', 'bundles/binary-daemon/dockerd', './cmd/dockerd']],
        status='unverified',
    )

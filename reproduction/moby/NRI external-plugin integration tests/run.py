import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import native_go

if __name__ == "__main__":
    native_go(__file__,
        repository='moby/moby',
        revision='6335222710d99b0311a0d0ceff604eb6f67d324d',
        package='./integration/daemon/nri',
        selector='^TestNRIContainerCreateEnvVarMod$/^env$/^set$',
        platform='linux',
        env={'GOFLAGS': '-mod=vendor', 'CGO_ENABLED': '1'},
        private_docker=True,
        requires=['DOCKER_INTEGRATION_DAEMON_DEST'],
        bin_dirs=['bundles/binary-daemon'],
        setup=[['go', 'build', '-o', 'bundles/binary-daemon/dockerd', './cmd/dockerd']],
        status='unverified',
    )

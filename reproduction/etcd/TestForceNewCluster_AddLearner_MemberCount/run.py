import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import BUILD_JOBS, go

GO_PROCESS_DEADLINE = '30m'

if __name__ == "__main__":
    go(__file__,
        repository='etcd-io/etcd',
        revision='32e390025bed53d5a4fa75db78a46b25c4e87bdd',
        package='./tests/e2e',
        selector='^TestForceNewCluster_AddLearner_MemberCount$',
        timeout=GO_PROCESS_DEADLINE,
        image='golang:1.27.3-bookworm@sha256:b08bc99468058b6d8a0ada17fa54996b910d5e82a7e95bee0372e3bd98415258',
        build=f'mkdir -p /opt/bin && go build -p={BUILD_JOBS} -o /opt/bin/etcd ./server && go build -p={BUILD_JOBS} -o /opt/bin/etcdctl ./etcdctl && go build -p={BUILD_JOBS} -o /opt/bin/etcdutl ./etcdutl && go test -c -p={BUILD_JOBS} -o /opt/test ./tests/e2e',
        test_flags='-bin-dir=/opt/bin',
        status='unverified',
    )

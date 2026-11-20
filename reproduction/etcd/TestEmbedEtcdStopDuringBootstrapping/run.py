import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

GO_PROCESS_DEADLINE = '15m'
CPU_QUOTA = 1
SOCKET_TMPFS_SIZE = '128m'

if __name__ == "__main__":
    go(__file__,
        repository='etcd-io/etcd',
        revision='e0c7b4d7eb9682c9cea733ae70dc0667d549c373',
        package='./tests/integration/embed',
        selector='^TestEmbedEtcd(AutoCompactionRetentionRetained|StopDuringBootstrapping)$',
        image='golang:1.26.0-bookworm@sha256:2a0ba12e116687098780d3ce700f9ce3cb340783779646aafbabed748fa6677c',
        flags='-race',
        prepare='RUN make gofail-enable',
        timeout=GO_PROCESS_DEADLINE,
        cpus=CPU_QUOTA,
        options=['--tmpfs', f'/src/tests/integration/embed:rw,nosuid,nodev,size={SOCKET_TMPFS_SIZE},mode=1777'],
        status='verified',
    )

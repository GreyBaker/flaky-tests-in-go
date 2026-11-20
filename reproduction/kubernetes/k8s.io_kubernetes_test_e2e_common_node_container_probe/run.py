import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import native_go

GO_PROCESS_DEADLINE = '30m'

if __name__ == "__main__":
    native_go(__file__,
        repository='kubernetes/kubernetes',
        revision='2d1b7de44e35cb7979bc17675a3b331a58a1e5d0',
        package='./test/e2e',
        selector='^TestE2E$',
        platform='linux',
        version='go1.27.2',
        env={'GOFLAGS': '-mod=vendor', 'CGO_ENABLED': '1'},
        requires=['KUBECONFIG'],
        timeout=GO_PROCESS_DEADLINE,
        test_flags=['--ginkgo.focus=should.*not.*be restarted with a non-local redirect http liveness probe', '--provider=local'],
        status='system dependency',
    )

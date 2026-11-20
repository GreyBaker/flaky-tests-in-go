import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

GO_PROCESS_DEADLINE = '180s'
CPU_QUOTA = 1
GO_THREADS = 1
MEMORY_LIMIT = '1g'

if __name__ == "__main__":
    go(__file__,
        repository='kubernetes/kubernetes',
        revision='faf3d6ca3d31cc790d81f56092d7947a282a419b',
        package='./pkg/controller/volume/attachdetach/reconciler',
        selector='^Test_Run_OneVolumeDetachOnOutOfServiceTaintedNode$',
        image='golang:1.27.2-bookworm@sha256:5cf287a799e6b94384bad13d16b14904c531f51ba65792237e122ce42b392f61',
        flags='-race',
        goflags='-mod=vendor',
        timeout=GO_PROCESS_DEADLINE,
        cpus=CPU_QUOTA,
        gomax=GO_THREADS,
        memory=MEMORY_LIMIT,
        options=['--memory-swap', MEMORY_LIMIT],
        status='unverified',
    )

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 100
CPU_QUOTA = 1
PINNED_CPU = '0'
PARALLEL_TESTS = 16

if __name__ == "__main__":
    go(__file__,
        repository='netdata/netdata',
        revision='d7ec424243bac7d7a6d750f4081bd86f1ecd7f2e',
        module='src/go',
        package='./plugin/agent/jobmgr/secrets',
        selector='^TestPreparedStoreOperationQuarantinesFailedUntakenMutationRelease$',
        image='golang:1.27.2-bookworm@sha256:5cf287a799e6b94384bad13d16b14904c531f51ba65792237e122ce42b392f61',
        batch=RUNS_PER_PROCESS,
        cpus=CPU_QUOTA,
        options=['--cpuset-cpus', PINNED_CPU],
        test_flags=f'-test.parallel={PARALLEL_TESTS} -test.shuffle=on',
        status='verified',
    )

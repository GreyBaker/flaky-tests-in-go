import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 100

if __name__ == "__main__":
    go(__file__,
        repository='netdata/netdata',
        revision='b20471f5d22e96055558de6d0ff78ecf23ba5677',
        module='src/go',
        package='./plugin/agent/jobmgr/joboutput',
        selector='^TestRuntimeStartupFailureDoesNotHideCleanupPanic$',
        image='golang:1.27.2-bookworm@sha256:5cf287a799e6b94384bad13d16b14904c531f51ba65792237e122ce42b392f61',
        batch=RUNS_PER_PROCESS,
        status='unverified',
    )

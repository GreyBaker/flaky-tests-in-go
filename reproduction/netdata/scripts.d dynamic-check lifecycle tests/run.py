import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 100

if __name__ == "__main__":
    go(__file__,
        repository='netdata/netdata',
        revision='c76d4113110363038f25c8bf0e8a4f2327431088',
        module='src/go',
        package='./plugin/scripts.d/collector/native',
        selector='^Test(DynamicChecks|ContractsOutputRejectionStillCommitsContract|Job_CriticalStartupAndRecovery)',
        image='golang:1.27.2-bookworm@sha256:5cf287a799e6b94384bad13d16b14904c531f51ba65792237e122ce42b392f61',
        batch=RUNS_PER_PROCESS,
        status='unverified',
    )

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

GO_PROCESS_DEADLINE = '180s'
CPU_QUOTA = 1
MEMORY_LIMIT = '1g'

if __name__ == "__main__":
    go(__file__,
        repository='kubernetes/kubernetes',
        revision='69b0ddb9132cc844955fe998d0b408ecc9bdac17',
        package='./pkg/scheduler/framework/preemption',
        selector='^TestPrepareCandidate$/^metrics:_compositepodgroup_preemptor_with_PDB_violations_and_disruptions_\\(Async_preemption_enabled:_true,_Async_API_calls_enabled:_true\\)$',
        image='golang:1.27.2-bookworm@sha256:5cf287a799e6b94384bad13d16b14904c531f51ba65792237e122ce42b392f61',
        flags='-race',
        goflags='-mod=vendor',
        timeout=GO_PROCESS_DEADLINE,
        cpus=CPU_QUOTA,
        memory=MEMORY_LIMIT,
        options=['--memory-swap', MEMORY_LIMIT],
        status='unverified',
    )

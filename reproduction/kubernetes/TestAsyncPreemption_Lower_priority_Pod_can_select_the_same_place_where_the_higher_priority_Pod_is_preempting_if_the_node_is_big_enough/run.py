import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

CPU_QUOTA = 1
MEMORY_LIMIT = '1g'

if __name__ == "__main__":
    go(__file__,
        repository='kubernetes/kubernetes',
        revision='a8a44c8869c1fb10ee69e7f241e3413a7ba328be',
        package='./test/integration/scheduler/preemption',
        selector='^TestAsyncPreemption$/^Lower_priority_Pod_can_select_the_same_place_where_the_higher_priority_Pod_is_preempting_if_the_node_is_big_enough$',
        image='golang:1.27.2-bookworm@sha256:5cf287a799e6b94384bad13d16b14904c531f51ba65792237e122ce42b392f61',
        flags='-race',
        goflags='-mod=vendor',
        etcd=True,
        cpus=CPU_QUOTA,
        memory=MEMORY_LIMIT,
        options=['--memory-swap', MEMORY_LIMIT],
        status='unverified',
    )

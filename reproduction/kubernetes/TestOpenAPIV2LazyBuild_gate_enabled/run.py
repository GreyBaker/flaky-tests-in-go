import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 10
GO_PROCESS_DEADLINE = '300s'
SHUFFLE_SEED = 42

if __name__ == "__main__":
    go(__file__,
        repository='kubernetes/kubernetes',
        revision='63eee90da226b6a813e58b2dac53c2fc2236481d',
        package='./test/integration/apiserver/openapi',
        selector='^TestOpenAPIV2(LazyBuild|CRDMergeNoDuplicateTypes)$',
        image='golang:1.27.2-bookworm@sha256:5cf287a799e6b94384bad13d16b14904c531f51ba65792237e122ce42b392f61',
        goflags='-mod=vendor',
        etcd=True,
        timeout=GO_PROCESS_DEADLINE,
        batch=RUNS_PER_PROCESS,
        test_flags=f'-test.short -test.shuffle={SHUFFLE_SEED}',
        options=['-e', 'KUBE_CACHE_MUTATION_DETECTOR=true', '-e', 'KUBE_PANIC_WATCH_DECODE_ERROR=false'],
        status='verified',
    )

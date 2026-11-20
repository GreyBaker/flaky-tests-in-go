import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import container

RUNS_PER_PROCESS = 10
GO_PROCESS_DEADLINE = '600s'
PACKAGE_JOBS = 4

if __name__ == "__main__":
    container(__file__,
        command=f"""\
set -e
export GOPATH=/scratch/gopath GOCACHE=/scratch/cache GOMODCACHE=/scratch/modules GOFIPS140=v1.0.0
exec go test -v -count="$COUNT" -timeout={GO_PROCESS_DEADLINE} -p={PACKAGE_JOBS} crypto/x509 crypto/internal/fips140/...
""",
        batch=RUNS_PER_PROCESS,
        writable=True,
        network='bridge',
        status='verified',
    )

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import container

GO_PROCESS_DEADLINE = '600s'

if __name__ == "__main__":
    container(__file__,
        command=f"""\
export GOPATH=/scratch/gopath GOCACHE=/scratch/cache GOMODCACHE=/scratch/modules
exec go test -v -count="$COUNT" -timeout={GO_PROCESS_DEADLINE} -run="^TestScript$/^mod_invalid_version$" cmd/go
""",
        writable=True,
        network='bridge',
        status='unverified',
    )

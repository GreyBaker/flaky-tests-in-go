import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 20

if __name__ == "__main__":
    go(__file__,
        repository='jesseduffield/lazygit',
        revision='62e1622f43520f0f8e252079692107f2cadf3ea0',
        package='./pkg/tasks',
        selector='^TestNewCmdTaskInstantStop$',
        goflags='-mod=vendor',
        image='golang:1.25.0-bookworm@sha256:81dc45d05a7444ead8c92a389621fafabc8e40f8fd1a19d7e5df14e61e98bc1a',
        batch=RUNS_PER_PROCESS,
        status='verified',
    )

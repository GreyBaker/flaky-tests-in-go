import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import native_go

RUNS_PER_PROCESS = 100

if __name__ == "__main__":
    native_go(__file__,
        repository='microsoft/TypeScript',
        revision='0c8f63f745ec8c8243c7d43d13e3f2fe8e04bc53',
        module='tsc',
        package='./internal/project',
        platform='win32',
        selector='^TestContentMapperInProject$/^trusted_workspace_transforms_the_content-mapped_file$',
        version='go1.27.2',
        batch=RUNS_PER_PROCESS,
        status='verified',
    )

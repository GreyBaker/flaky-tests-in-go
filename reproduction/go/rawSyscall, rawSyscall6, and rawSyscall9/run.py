import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import native_go

if __name__ == "__main__":
    native_go(__file__,
        repository='golang/go',
        revision='7239eead280fdf78b47a37d7df218d5331155c17',
        package='os/exec',
        selector='.',
        platform='darwin',
        toolchain_source=True,
        flags='-race',
        status='system dependency',
    )

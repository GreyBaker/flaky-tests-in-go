import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import native_go

GO_PROCESS_DEADLINE = '180s'

if __name__ == "__main__":
    native_go(__file__,
        repository='gohugoio/hugo',
        revision='3a11d22da365434ee47df818371d4f32a397b73d',
        package='.',
        platform='win32',
        version='go1.24.0',
        selector='^TestCommands$/^mod_npm_withexisting$',
        timeout=GO_PROCESS_DEADLINE,
        status='unverified',
    )

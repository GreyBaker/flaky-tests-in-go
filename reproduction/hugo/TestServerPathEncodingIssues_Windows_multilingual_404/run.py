import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

GO_PROCESS_DEADLINE = '120s'

if __name__ == "__main__":
    go(__file__,
        repository='gohugoio/hugo',
        revision='b002d47953e341b6c84e39001d312bd95a3b5078',
        package='./commands',
        selector='^TestServerPathEncodingIssues$/^Windows_multilingual_404$',
        image='golang:1.19.13-bookworm@sha256:da9da58d86d106a5dda2ce249b00cf3b31cdd626ea41597e476de7b4eebad8c4',
        timeout=GO_PROCESS_DEADLINE,
        status='verified',
    )

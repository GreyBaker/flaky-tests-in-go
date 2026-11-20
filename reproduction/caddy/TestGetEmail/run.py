import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

if __name__ == "__main__":
    go(__file__,
        repository='caddyserver/caddy',
        revision='f46da403d85e331fee2763d3704969f4ec92ebf8',
        package='./caddytls',
        selector='^TestGetEmail$',
        goflags='',
        image='golang:1.11.13-stretch@sha256:f6b90217127a64afbc2380f06fd0d0193f254be0975bc69ba664cbf06a1892e4',
        source='/go/src/github.com/mholt/caddy',
        prepare='ENV GO111MODULE=off CGO_ENABLED=0',
        scratch='disk',
        status='verified',
    )

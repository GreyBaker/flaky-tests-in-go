import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import container

PTY_ROWS = 100
PTY_COLUMNS = 150

if __name__ == "__main__":
    container(__file__,
        command=f"""\
export TERM=xterm-256color
exec script -q -e -c 'stty rows {PTY_ROWS} cols {PTY_COLUMNS}; /opt/integration-cli cli diff/diff_commits' /dev/null
""",
        writable=True,
        user='0:0',
        options=['-e', 'GOCACHE=/root/.cache/go-build'],
        tmpfs_tmp=False,
        status='verified',
    )

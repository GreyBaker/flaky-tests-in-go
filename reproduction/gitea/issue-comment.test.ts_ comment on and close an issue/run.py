import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import container

TEST_USER = '1000:1000'
SHM_LIMIT = '1g'
BROWSER_WORKERS = 1

if __name__ == "__main__":
    container(__file__,
        command=f'exec bash tools/test-e2e.sh run tests/e2e/issue-comment.test.ts --project=firefox --workers={BROWSER_WORKERS} --repeat-each="$COUNT" --reporter=list',
        user=TEST_USER,
        options=['--mount', 'type=volume,target=/src', '--shm-size', SHM_LIMIT],
        writable=True,
        status='unverified',
    )

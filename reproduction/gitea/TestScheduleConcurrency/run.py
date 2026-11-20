import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import DEFAULT_TEST_PARALLELISM, DEFAULT_TEST_TIMEOUT, container

TEST_USER = '1000:1000'
SHM_LIMIT = '1g'

if __name__ == "__main__":
    container(__file__,
        command=f"""\
set -e
export GITEA_TEST_ROOT=/src GITEA_TEST_CONF=tests/sqlite.ini TEST_LDAP=1
cd /src
make generate-ini-sqlite
exec /opt/test -test.v -test.count="$COUNT" -test.parallel={DEFAULT_TEST_PARALLELISM} -test.timeout={DEFAULT_TEST_TIMEOUT} -test.run='^TestScheduleConcurrency$'
""",
        user=TEST_USER,
        options=['--mount', 'type=volume,target=/src', '--shm-size', SHM_LIMIT],
        writable=True,
        status='unverified',
    )

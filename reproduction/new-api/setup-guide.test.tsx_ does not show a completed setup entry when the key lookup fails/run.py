import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import container

FRONTEND_WORKERS = 4

if __name__ == "__main__":
    container(__file__,
        command=f'exec bun run test src/features/dashboard/components/overview/__tests__/setup-guide.test.tsx --maxWorkers={FRONTEND_WORKERS} --reporter=verbose',
        user='0:0',
        writable=True,
        status='unverified',
    )

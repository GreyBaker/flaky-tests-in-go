import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import container

FRONTEND_WORKERS = 4

if __name__ == "__main__":
    container(__file__,
        command=f'exec bun run test src/features/channels/components/__tests__/channel-configuration.test.tsx src/features/system-settings/models/__tests__/visual-billing-editor.test.tsx --maxWorkers={FRONTEND_WORKERS} --reporter=verbose',
        user='0:0',
        writable=True,
        status='unverified',
    )

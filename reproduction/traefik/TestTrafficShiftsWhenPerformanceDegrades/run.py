import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 10

if __name__ == "__main__":
    go(__file__,
        repository='traefik/traefik',
        revision='72ba481bbc887580dcdf8e331b820605ec75ab67',
        package='./pkg/server/service/loadbalancer/leasttime',
        selector='^TestTrafficShiftsWhenPerformanceDegrades$',
        batch=RUNS_PER_PROCESS,
        status='unverified',
    )

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _runner import go

RUNS_PER_PROCESS = 100

if __name__ == "__main__":
    go(__file__,
        repository='traefik/traefik',
        revision='cabcf19303231e62f57aa62d2da6c83105711910',
        package='./pkg/server/service/loadbalancer/hrw',
        selector='^Test(Balancer|BalancerDownThenUp|BalancerPropagate|Sticky)$',
        batch=RUNS_PER_PROCESS,
        status='verified',
    )

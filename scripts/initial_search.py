from collections import Counter, deque
import csv
import math
import os
from pathlib import Path
import time


import requests

REPOSITORIES = [
    "ollama/ollama", "golang/go", "kubernetes/kubernetes", "microsoft/TypeScript",
    "fatedier/frp", "infiniflow/ragflow", "gohugoio/hugo", "syncthing/syncthing",
    "gin-gonic/gin", "junegunn/fzf", "jesseduffield/lazygit", "netdata/netdata",
    "caddyserver/caddy", "nektos/act", "moby/moby", "prometheus/prometheus", "traefik/traefik",
    "usememos/memos", "pocketbase/pocketbase", "rclone/rclone", "go-gitea/gitea",
    "etcd-io/etcd", "ethereum/go-ethereum", "quantumnous/new-api"
] # none from gonic/gin, fatedier/frp, infiniflow/ragflow, nektos/act, pocketbase/pocketbase, 

TITLE_EXPRESSION = "((flaky in:title) OR (flake in:title) OR (flaking in:title) OR (flakiness in:title)) AND (test in:title)"
RESULTS_PER_CELL = 20
SINCE, AS_OF = "2013-01-01", "2026-10-22" # this is fine, we still implicitly pull the RESULTS_PER_CELL most recent per category
MAX_REQUESTS = 100 
REQUEST_INTERVAL = 6.0 
MAX_RATE_LIMIT_RETRIES = 3 
MAX_RATE_LIMIT_WAIT = 60 

OUTPUT_FILE = Path(__file__).resolve().parent / "pre-candidates.csv"

def make_searches():
    jobs = []

    for _, repo in enumerate(dict.fromkeys(REPOSITORIES)):
        for kind in ("issue", "pull_request"):
            jobs.append({"repository": repo, "kind": kind, "scheme": "boolean_title", "text": TITLE_EXPRESSION, "start": SINCE, "end": AS_OF,
                        "advanced_search": True,
                        "query": f"repo:{repo} {TITLE_EXPRESSION} type:{'pr' if kind == 'pull_request' else 'issue'} created:{SINCE}..{AS_OF}",
                        "page": 1, "total_count": 0, "unique_items": 0, "incomplete": False, "status": "pending"})
    return jobs


def cell_key(job: dict) -> tuple:
    """Pulls out the information we usually need"""
    return job["repository"], job["kind"], job["start"], job["end"]

def rate_limit_delay(envelope):
    headers = {key.lower(): value for key, value in envelope.get("headers", {}).items()}
    try:
        if envelope["status"] in (403, 429) and "retry-after" in headers:
            delay = float(headers["retry-after"]) + 2
        elif (envelope["status"] in (403, 429) and headers.get("x-ratelimit-remaining") == "0"
              and headers.get("x-ratelimit-resource") == "search"):
            delay = float(headers["x-ratelimit-reset"]) - time.time() + 2
        else:
            return None
    except (ValueError, KeyError, TypeError):
        return None
    if not math.isfinite(delay):
        return None
    return min(max(1, delay), MAX_RATE_LIMIT_WAIT)


def csv_cell(value):
    if value is None:
        return ""
    text = str(value)
    # avoid some spreadsheet issues
    return "'" + text if text.lstrip().startswith(("=", "+", "-", "@")) or text.startswith(("\t", "\r")) else text


jobs = make_searches()
planned_cells = {cell_key(job) for job in jobs}
candidates, seen_by_cell = {}, {}
request_count, rate_limit_retries = 0, 0
queue = deque(jobs)
session = requests.Session()
session.headers.update({"User-Agent": "go-flaky-initial-search", "Accept": "application/vnd.github.text-match+json", "X-GitHub-Api-Version": "2022-11-28"})
token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
if token:
    session.headers["Authorization"] = f"Bearer {token}"
try:
    while queue:
        job = queue.popleft()
        cell_urls = seen_by_cell.setdefault(cell_key(job), set())
        remaining = RESULTS_PER_CELL - len(cell_urls)
        if remaining <= 0:
            job["status"] = "cell_limit_reached"  # No request; keep the skipped query in coverage.
            continue
        if request_count >= MAX_REQUESTS:
            break
        endpoint = "issues"  # GitHub serves both typed issue and PR queries here.
        params = {"q": job["query"], "advanced_search": "true", "sort": "created", "order": "desc", "per_page": remaining, "page": 1}
        job["requested_items"] = remaining
        time.sleep(REQUEST_INTERVAL)
        request_count += 1
        envelope = {}
        try:
            response = session.get(f"https://api.github.com/search/{endpoint}", params=params, timeout=30)
            envelope.update(status=response.status_code, headers=dict(response.headers))
        except requests.RequestException as exc:
            envelope.update(status=None, error=str(exc))
        if envelope["status"] != 200:
            job.update(status="error", error=envelope.get("error", f"HTTP {envelope['status']}"))
            print(f"[{request_count}/{MAX_REQUESTS}] {job['repository']}: {job['error']}")
            if envelope["status"] in (403, 429):
                delay = rate_limit_delay(envelope)
                if delay is not None and rate_limit_retries < MAX_RATE_LIMIT_RETRIES and request_count < MAX_REQUESTS:
                    rate_limit_retries += 1
                    job["rate_limit_retries"] = job.get("rate_limit_retries", 0) + 1
                    print(f"waiting {delay:.1f}s before retry {rate_limit_retries}/{MAX_RATE_LIMIT_RETRIES}")
                    time.sleep(delay)
                    queue.appendleft(job)
                    continue
                break
            continue
        try:
            result = response.json()
            job.pop("error", None)
            items, total = result["items"], result["total_count"]
            if not isinstance(items, list) or type(total) is not int or total < 0:
                raise ValueError("Unexpected search response schema")
            job["total_count"] = total
            job["incomplete"] = bool(result.get("incomplete_results"))
            urls, scope_errors = set(), []
            if len(items) > remaining:
                raise ValueError("Response exceeded the requested per-cell limit")
            for item in items:
                url = item["html_url"].split("#", 1)[0]
                urls.add(url)
                cell_urls.add(url)
                record = candidates.setdefault(url, {"repository": job["repository"], "kind": job["kind"], "validation_status": "unreviewed", "item": item, "matches": []})
                record["matches"].append({"query": job["query"], "scheme": job["scheme"], "page": job["page"]})
            job["unique_items"] = len(urls)
            if scope_errors:
                job.update(status="error", error="Returned URLs outside the requested repository/type", unexpected_urls=scope_errors)
            elif job["incomplete"]:
                job["status"] = "incomplete"
            elif len(items) < min(total, remaining) or len(urls) < len(items):
                job["status"] = "short_page"
            else:
                job["status"] = "limited" if total > len(urls) else "complete"
            print(f"[{request_count}/{MAX_REQUESTS}] {job['repository']} {job['kind']} {job['scheme']} page {job['page']}: {len(items)} found")
        except (ValueError, KeyError, TypeError) as exc:
            job.update(status="error", error=str(exc))
            continue

except KeyboardInterrupt:
    pass
except Exception:
    raise
finally:
    session.close()
    for job in jobs:
        if job["status"] == "pending" and len(seen_by_cell.get(cell_key(job), set())) >= RESULTS_PER_CELL:
            job["status"] = "cell_limit_reached"

    # save results
    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "repository", "kind", "title", "created at", "closed at", "state", "description"])
            for url, record in candidates.items():
                item = record["item"]
                writer.writerow([csv_cell(value) for value in [url, record["repository"], record["kind"], item.get("title"),
                                 item.get("created_at"), item.get("closed_at"), item.get("state"), item.get("body")]])
    

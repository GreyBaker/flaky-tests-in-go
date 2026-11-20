# An Analysis of Flaky Tests in Popular Go Projects

This repository holds scripts, data, and presentations regarding the work "An Analysis of Flaky Tests in Popular Go Projects".

## Building the Database

Run `python initial_search.py` to generate `pre-candidates.csv`. 

Run `SELECT a.URL + " ", a.repository, a.title, a['closed at'] ORDER BY a.repository, a['closed at'] DESC` where `pre-candidates` is table `a` and rename column 1 to 'URL' to replicate transformation into the `no-description-pre-candidates.csv` verison. In this version, items which are inspected and found to be closed unsuccessfully are removed for better review later. 

For both of those, interpretation follows that URL refers to the GitHub URL source of the entry, which effectively is the primary key. Within that we identify the repository related, the title of the item as given by the GitHub entry, and timestamps regarding its closure in ISO8601 format. `pre-candidates.csv` also carries a copy of the description of the entry as present on GitHub.

`candidates.csv` instead carries the repository and title as primary, then offers potentially both of issue URL and code URL, then the closed at time. Manual modification is then made to separate code and issue URLs, to combine items, and to reorder into repository primacy order. 

`categorization.csv` also carries information regarding the various categorizations employed in the course of the project. The flake and nature categorizations largely refer to the table in [Understanding Flaky Tests: The Developer’s Perspective](https://arxiv.org/pdf/1907.01466v1).

## Database Processing

Information and scripts pertaining to replications of flakiness can be found in `replication/` 

Categorization findings can be seen summarized in `categorization.csv`.

## Reproduction

Scripts share `_runner.py`. Example usage:
```sh
python reproduction/caddy/TestGetEmail/run.py --runs 500 --seconds 3600
```

Exit codes: 0 passed, 1 subject failure, 2 setup error, 124 outer cutoff—not a reproduced timeout.

Requires Python 3.10+, Docker, Git, Go, upstream build tools and the platform specified in their script.

Service cases need disposable infrastructure:
- Ollama: a daemon built from the pinned revision at `OLLAMA_HOST`, with `llama3.2:1b`.
- Kubernetes probes: a real cluster selected by `KUBECONFIG`.
- Moby/Memos: a private Unix-socket daemon in `DOCKER_HOST`. Moby also needs matching runtime tools, fixtures and `DOCKER_INTEGRATION_DAEMON_DEST`.

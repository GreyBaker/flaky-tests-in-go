This repository holds scripts, data, and presentations regarding the work "An Analysis of Flaky Tests in Popular Go Projects".

## Building the Database

Run `python initial_search.py` to generate `pre-candidates.csv`. Remove the descriptions column and add a space at the start of the second column to replicate transformation into the `no-description-pre-candidates.csv` verison.

For both of those and `candidates.csv`, interpretation follows that URL refers to the GitHub URL source of the entry, which effectively is the primary key. Within that we identify the repository related, the kind (either a pull request or a GitHub issue), the title of the item as given by the GitHub entry, timestamps regarding its existence and resolution in ISO8601 format, and state on GitHub (referring to open/closed). `pre-candidates.csv` also carries a copy of the description of the entry as present on GitHub.

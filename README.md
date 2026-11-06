This repository holds scripts, data, and presentations regarding the work "An Analysis of Flaky Tests in Popular Go Projects".

## Building the Database

Run `python initial_search.py` to generate `pre-candidates.csv`. 

Run `SELECT a.URL + " ", a.repository, a.title, a['closed at'] ORDER BY a.repository, a['closed at'] DESC` where `pre-candidates` is table `a` and rename column 1 to 'URL' to replicate transformation into the `no-description-pre-candidates.csv` verison. In this version, items which are inspected and found to be closed unsuccessfully are removed for better review later. 

For both of those, interpretation follows that URL refers to the GitHub URL source of the entry, which effectively is the primary key. Within that we identify the repository related, the title of the item as given by the GitHub entry, and timestamps regarding its closure in ISO8601 format. `pre-candidates.csv` also carries a copy of the description of the entry as present on GitHub.

`candidates.csv` instead carries the repository and title as primary, then offers potentially both of issue URL and code URL, then the closed at time. Manual modification is then made to separate code and issue URLs, to combine items, to carry discovery state, and to reorder into repository primacy order. 



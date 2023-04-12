# WikiRunner
Quick wikipedia speedrunner bot. Requires [beautiful soup](https://beautiful-soup-4.readthedocs.io/en/latest/#installing-beautiful-soup) and [requests](https://docs.python-requests.org/en/latest/user/install/).

Usage: python wikirunner.py SourcePageName DestinationPageName bfs/dfs LogPages

Replace SourcePageName and DestinationPageName with your desired source and destination

Specify bfs or dfs as the third argument (bfs/dfs); if no argument is provided, runner will default to bfs.

If you want a log of the pages accessed to print out while running, set the 4th argument (LogPages) to 1.

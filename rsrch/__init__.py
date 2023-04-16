from ._src.rsrch import download_papers, push_papers

# Make the functions accessible with from rsrch import *
__all__ = ["download_papers", "push_papers"]

# Make the functions directly accessible under the package namespace
download_papers = download_papers
push_papers = push_papers

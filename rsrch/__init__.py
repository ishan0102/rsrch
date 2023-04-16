from ._src.rsrch import download, upload

# Make the functions accessible with from rsrch import *
__all__ = ["download", "upload"]

# Make the functions directly accessible under the package namespace
download = download
upload = upload

from ._src.notion import download, upload
from ._src.labml import popular

# Make the functions accessible with from rsrch import *
__all__ = ["download", "upload", "popular"]

# Make the functions directly accessible under the package namespace
download = download
upload = upload
popular = popular

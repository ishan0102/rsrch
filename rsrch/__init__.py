from ._src.notion import RsrchClient

# Make the client accessible with from rsrch import *
__all__ = ["RsrchClient"]

# Make the client accessible with from rsrch import RsrchClient
RsrchClient = RsrchClient

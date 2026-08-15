"""
Presentation configuration.
"""

from .cors import configure_cors
from .gzip import configure_gzip
from .openapi import configure_openapi
from .security import configure_security
from .trusted_hosts import configure_trusted_hosts
from .versioning import configure_versioning

__all__ = [
    "configure_cors",
    "configure_gzip",
    "configure_openapi",
    "configure_security",
    "configure_trusted_hosts",
    "configure_versioning",
]
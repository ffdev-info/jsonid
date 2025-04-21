"""jsonid version information. """

from importlib.metadata import PackageNotFoundError, version
from typing import Final

# Store time format in version for consistent meta output.
UTC_TIME_FORMAT: Final[str] = "%Y-%m-%dT%H:%M:%SZ"


def get_version():
    """Return information about the version of this application. If
    it returns 0.0.0 then the user is to assume this is a development
    version. Otherwise the version must be driven by the source
    control management through appropriate tagging.
    """
    __version__ = "0.0.0"
    try:
        __version__ = version("jsonid")
    except PackageNotFoundError:
        # package is not installed
        pass
    return __version__

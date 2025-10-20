"""Configure testing."""

from typing import Final

from src.jsonid import jsonid

DEBUG: Final[bool] = False

jsonid.init_logging(DEBUG)

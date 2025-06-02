"""Simple module to analys JSON for technical metadata."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def analyse_input(data: Any):
    """Analyse a given input and output statistics, e.g.

    * No. keys at top level.
    * Keys at top level.
    * Key-types at top level.
    * Possibly deopt of keys at top-level.
    * Possibly total depth (recursive).

    """
    logger.debug("analysing: %s", data)

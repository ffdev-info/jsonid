"""Code helperrs."""

import logging
import time

logger = logging.getLogger(__name__)


def _function_name(func: str) -> str:
    """Attemptt to retrieve function name for timeit."""
    return str(func).rsplit("at", 1)[0].strip().replace("<function", "def ").strip()


def timeit(func):
    """Decorator to output the time taken for a function"""

    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        func_name = _function_name(str(func))
        # pylint: disable=W1203
        logger.debug(f"Time taken: {elapsed:.6f} seconds ({func_name}())")
        return result

    return wrapper

"""Code helperrs."""

import logging
import time

try:
    import registry_data
except ModuleNotFoundError:
    try:
        from src.jsonid import registry_data
    except ModuleNotFoundError:
        from jsonid import registry_data


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
        func_name = _function_name(str(func)).strip()
        # pylint: disable=W1203
        logger.debug(f"Time taken: {elapsed:.6f} seconds ({func_name}())")
        return result

    return wrapper


def entry_check() -> bool:
    """Make sure the entries are all unique."""
    data = registry_data.registry()
    ids = [datum.identifier for datum in data]
    return len(set(ids)) == len(data)

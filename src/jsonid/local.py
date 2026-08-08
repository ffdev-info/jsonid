"""Functions supporting local registry use"""

import logging
import pathlib
import tomllib as toml

logger = logging.getLogger(__name__)


class LocalRegistryException(Exception):
    """Exception to raise if something goes wrong with the local
    registry.
    """


def load_and_parse_local_registry(path: str):
    """Read the data use the data."""

    registry = pathlib.Path(path)
    if not registry.exists():
        raise LocalRegistryException("registry path not found")

    load_local_registry(registry)


def load_local_registry(registry: pathlib.Path):
    """Load the local registry and return it as a data structure
    to the caller.
    """

    with registry.open() as data:
        registry_data = data.read()

    reg = toml.loads(registry_data)

    logger.debug("local registry length: %d", len(reg["entries"]))

    assert False

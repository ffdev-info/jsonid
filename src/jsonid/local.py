"""Functions supporting local registry use"""

import copy
import logging
import pathlib
import tomllib as toml

try:
    import registry_class
    import registry_data
except ModuleNotFoundError:
    try:
        from src.jsonid import registry_class, registry_data
    except ModuleNotFoundError:
        from jsonid import registry_class, registry_data

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


"""
    registry_class.RegistryEntry(
        identifier="jrid:0001",
        name=[{"@en": "JavaScript Package Lock"}],
        description=[{"@en": "describes an exact Node (NPM) module dependency tree"}],
        markers=[
            {"KEY": "name", "EXISTS": None},
            {"KEY": "lockfileVersion", "EXISTS": None},
            {"KEY": "packages", "EXISTS": None},
        ],
    ),
"""


def load_local_registry(registry: pathlib.Path, only_local: bool = False):
    """Load the local registry and return it as a data structure
    to the caller.
    """

    with registry.open() as data:
        local_registry_data = data.read()

    local_reg_config = toml.loads(local_registry_data)

    logger.debug("local registry length: %d", len(local_reg_config["entries"]))

    local_reg = []

    for item in local_reg_config["entries"]:

        # TODO: cleanup, ensure keys are capitalized.
        m = []
        for i in item["markers"]:
            d = {}
            for k, v in tuple(i.items()):
                d.update({k.upper(): v})
            m.append(d)

        # TODO: variable naming.
        a = registry_class.RegistryEntry(
            identifier=item["identifier"],
            name=[{"@en": item.get("name")}],
            description=[{"@en": item.get("description")}],
            markers=m,
        )

        print(a)
        print(a.markers)
        print("---")
        # if local...
        local_reg.append(a)

    if only_local:
        return local_reg

    reg = copy.deepcopy(registry_data.registry())

    return reg + local_reg

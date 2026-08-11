"""Test functions associated with the local registry."""

from typing import Final

from src.jsonid import local

registry: Final[
    str
] = """
[[entries]]

name = "doctype1"
identifier = "local0001"

[[entries.markers]]

key = "key1"
is = "value1"

[[entries.markers]]

key = "key2"
is = "value2"

[[entries]]

name = "doctype2"
identifier = "local0002"

[[entries.markers]]

key = "key2"
is = "value2"

"""


def test_load_local(tmp_path):
    """Ensure loading the local registry works as anticipated."""

    a = tmp_path / "registry_path"
    a.write_text(registry)

    local.load_local_registry(a)

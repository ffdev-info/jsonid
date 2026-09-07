"""Test functions associated with the local registry."""

import copy
import tomllib
from typing import Final

import pytest

from src.jsonid import local, registry_data, registry, file_processing

local_registry: Final[str] = """
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
description = "description TODO"

[[entries.markers]]

key = "key2"
is = "value2"

"""

test_file = """
{
 "key2": "value2"
}
"""


def test_load_local(tmp_path):
    """Ensure loading the local registry and combining it with the
    inbuilt registry works as anticipated."""

    reg = copy.deepcopy(registry_data.registry())
    local_reg_path = tmp_path / "registry_path"
    local_reg_path.write_text(local_registry)
    local_reg_conf = tomllib.loads(local_registry)
    assert len(reg) != len(local_reg_conf["entries"])
    local_reg = local.load_local_registry(local_reg_path)
    assert len(local_reg) == len(reg) + len(local_reg_conf["entries"])


@pytest.mark.asyncio
async def test_load_local_only(tmp_path):
    """Ensure that just loading the local registry works as
    anticipated.
    """

    local_reg_path = tmp_path / "registry_path"
    local_reg_path.write_text(local_registry)
    local_reg_conf = tomllib.loads(local_registry)
    local_reg = local.load_local_registry(local_reg_path, only_local=True)
    assert len(local_reg) == len(local_reg_conf["entries"])

    test_file_path = tmp_path / "test_file.json"
    test_file_path.write_text(test_file)

    base_obj = await file_processing.identify_plaintext_bytestream(
        path=test_file_path,
        strategy=["JSON"],
    )

    id_ = registry.matcher(
        base_obj=base_obj,
        reg_data=local_reg,
    )

    print(id_)

    assert len(id_) == 1
    assert id_[0].identifier == "local0002"
    assert id_[0].name[0]["@en"] == "doctype2"

    assert False

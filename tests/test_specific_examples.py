"""Test specific examples from the registry. """

# pylint: disable=C0103

import json

import pytest

from src.jsonid import registry, registry_data

specific_registry = [
    registry_data.RegistryEntry(
        identifier="id0019",
        name=[{"@en": "JSON Patch RFC 6902"}],
        markers=[
            {"INDEX": 0, "KEY": "op", "EXISTS": None},
            {"INDEX": 0, "KEY": "path", "EXISTS": None},
        ],
    ),
]

json_patch = """
   [
     { "op": "test", "path": "/a/b/c", "value": "foo" },
     { "op": "remove", "path": "/a/b/c" },
     { "op": "add", "path": "/a/b/c", "value": [ "foo", "bar" ] },
     { "op": "replace", "path": "/a/b/c", "value": 42 },
     { "op": "move", "from": "/a/b/c", "path": "/a/b/d" },
     { "op": "copy", "from": "/a/b/d", "path": "/a/b/e" }
   ]

"""


specific_tests = [
    (specific_registry, json_patch, "id0019"),
]


@pytest.mark.parametrize("test_registry, test_data, expected_id", specific_tests)
def test_specific(mocker, test_registry, test_data, expected_id):
    """Test specific examples that have been challenging."""
    mocker.patch("src.jsonid.registry_data.registry", return_value=test_registry)
    try:
        json_loaded = json.loads(test_data)
    except json.JSONDecodeError as err:
        assert False, f"data won't decode as JSON: {err}"
    res = registry.matcher(json_loaded)
    assert res[0].identifier == expected_id


depth_test_1 = {
    "children": [
        {
            "name": "product service",
            "children": [
                {"name": "price", "children": [{"name": "cost", "size": 8}]},
                {"name": "quality", "children": [{"name": "messaging", "size": 4}]},
            ],
        },
        {
            "name": "customer service",
            "children": [
                {"name": "Personnel", "children": [{"name": "CEO", "size": 7}]}
            ],
        },
        {
            "name": "product",
            "children": [
                {"name": "Apple", "children": [{"name": "iPhone 4", "size": 10}]}
            ],
        },
    ]
}


specific_tests = [
    (depth_test_1, 7),
]


@pytest.mark.parametrize("depth_test, expected_depth", specific_tests)
def test_get_depth(depth_test, expected_depth):
    """Assert depth tests work."""
    assert registry.get_depth(depth_test) == expected_depth

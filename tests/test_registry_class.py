"""Tests for the registry class object."""

import pytest

from src.jsonid import registry_class

registry_marker_tests = [
    (
        [
            {"KEY": "$id", "STARTSWITH": "http://www.parcore.org/schema/"},
            {"KEY": "$schema", "EXISTS": None},
            {"KEY": "definitions", "ISTYPE": dict},
        ],
        {
            "identifier": "",
            "name": [],
            "version": None,
            "description": [],
            "pronom": "",
            "wikidata": "",
            "loc": "",
            "archive_team": "",
            "rfc": "",
            "mime": [],
            "markers": [
                {"KEY": "$id", "STARTSWITH": "http://www.parcore.org/schema/"},
                {"KEY": "$schema", "EXISTS": None},
                {"KEY": "definitions", "ISTYPE": "map"},
            ],
            "depth": 0,
            "additional": "",
            "encoding": "",
        },
    ),
    (
        [
            {"KEY": "$id", "STARTSWITH": "http://www.parcore.org/schema/"},
            {"KEY": "$schema", "EXISTS": None},
            {"KEY": "definitions", "ISTYPE": None},
        ],
        {
            "identifier": "",
            "name": [],
            "version": None,
            "description": [],
            "pronom": "",
            "wikidata": "",
            "loc": "",
            "archive_team": "",
            "rfc": "",
            "mime": [],
            "markers": [
                {"KEY": "$id", "STARTSWITH": "http://www.parcore.org/schema/"},
                {"KEY": "$schema", "EXISTS": None},
                {"KEY": "definitions", "ISTYPE": None},
            ],
            "depth": 0,
            "additional": "",
            "encoding": "",
        },
    ),
    (
        [],
        {
            "identifier": "",
            "name": [],
            "version": None,
            "description": [],
            "pronom": "",
            "wikidata": "",
            "loc": "",
            "archive_team": "",
            "rfc": "",
            "mime": [],
            "markers": [],
            "depth": 0,
            "additional": "",
            "encoding": "",
        },
    ),
]


@pytest.mark.parametrize("entry, expected", registry_marker_tests)
def test_registry_entry_markers_json(entry, expected):
    """Outputting the markers as JSON requires some subtle changes to
    types so they can be stringified correctly. Test these work as
    throughout any changes to the code base.
    """
    entry_obj = registry_class.RegistryEntry()
    entry_obj.markers = entry
    res = entry_obj.json()
    assert res == expected

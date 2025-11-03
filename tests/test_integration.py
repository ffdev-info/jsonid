"""Provide some integration testing to ensure consistency of reporting
outputs from the tool.

It is important we test the CLI output of the tool. From the different
files that might be given to JSONID, we expect the following MIMETypes.

- application/octet-stream; charset=binary
- inode/x-empty; charset=binary (empty file)
- application/json; charset=<encoding>
- application/jsonl
- application/jsonl+<suffix>

MIMETypes should align with Linux's `$file` command if there is any
divergence we must first check if it is by design, e.g. in the case
of JSONL we do provide a mime+suffix and `$file` does not. Other
divergences should be investigated and JSONID brought into alignment.

"""

# pylint: disable=C0103

import sys
from typing import Final

import pytest

from src.jsonid import file_processing, jsonid, registry_class

integration_tests: Final[list] = [
    (
        # JSON example: {"test": "1"} .
        b"\x7b\x22\x74\x65\x73\x74\x22\x3a\x20\x22\x31\x22\x7d\x0a",
        'test_file.json\t[1]\tapplication/json; charset=UTF-8; doctype="JavaScript Object Notation (JSON)"; ref=jrid:JSON',
    ),
    (
        # Binary example: just binary .
        b"\x07\x00\x10",
        "test_file.json\t[1]\tapplication/octet-stream; charset=binary",
    ),
    (
        # Text example: just text (-#123).
        b"\x20\x20\x2D\x23\x31\x32\x33",
        "test_file.json\t[1]\ttext/plain; charset=unknown",
    ),
    (
        # TOML example: just text (#123).
        b"\x23\x31\x32\x33",
        'test_file.json\t[1]\tapplication/toml; charset=UTF-8; doctype="Tom\'s Obvious, Minimal Language (TOML)"; ref=jrid:TOML',
    ),
    (
        # JSON: utf16-LE
        b"\x7b\x00\x22\x00\x61\x00\x22\x00\x3a\x00\x20\x00\x22\x00\x62\x00\x22\x00\x7d\x00\x0a\x00",
        'test_file.json\t[1]\tapplication/json; charset=UTF-16; doctype="JavaScript Object Notation (JSON)"; ref=jrid:JSON',
    ),
    (
        # JSON: utf16-BE
        b"\x00\x7b\x00\x22\x00\x61\x00\x22\x00\x3a\x00\x20\x00\x22\x00\x62\x00\x22\x00\x7d\x00\x0a",
        'test_file.json\t[1]\tapplication/json; charset=UTF-16BE; doctype="JavaScript Object Notation (JSON)"; ref=jrid:JSON',
    ),
    (
        # Empty file.
        b"",
        "test_file.json\t[1]\tinode/x-empty; charset=binary",
    ),
    (
        # Just open/close parenthesis.
        b"\x7b\x7d",
        'test_file.json\t[1]\tapplication/json; charset=UTF-8; doctype="JavaScript Object Notation (JSON)"; ref=jrid:JSON',
    ),
    (
        # JSONL.
        b"\x1f\x8b\x08\x08\xd1\x94\x02\x69\x00\x03\x73\x69\x6d\x70\x6c\x65\x2e\x6a\x73\x6f\x6e\x00\xab\xae\xe5\xaa\xae\xe5\x02\x00\xaf\xf1\x38\x9c\x06\x00\x00\x00",
        'test_file.json\t[1]\tapplication/jsonl+gzip; charset=UTF-8; doctype="JSONLines (JSONL)"; ref=jrid:JSONL',
    ),
    (
        # Uncompressed JSONL.
        b"\x7b\x7d\x0a\x7b\x7d\x0a",
        'test_file.json\t[1]\tapplication/jsonl; charset=UTF-8; doctype="JSONLines (JSONL)"; ref=jrid:JSONL',
    ),
    (
        # BZIP2 JSONL.
        b"\x42\x5a\x68\x39\x31\x41\x59\x26\x53\x59\xcb\xf5\x6c\xd6\x00\x00\x01\xc0\x80\x00\x10\x00\x0a\x20\x00\x21\x26\x41\x98\x84\x8e\x2e\xe4\x8a\x70\xa1\x21\x97\xea\xd9\xac",
        'test_file.json\t[1]\tapplication/jsonl+x-bzip2; charset=UTF-8; doctype="JSONLines (JSONL)"; ref=jrid:JSONL',
    ),
    (
        # GZIP: not JSONL
        b"\x1f\x8b\x08\x08\x8c\x98\x02\x69\x00\x03\x66\x69\x6c\x65\x00\x4b\x49\x2c\x49\xe4\x02\x00\x82\xc5\xc1\xe6\x05\x00\x00\x00",
        "test_file.json\t[1]\tapplication/gzip; charset=binary",
    ),
    (
        # BZIP2 not JSONL
        b"\x42\x5a\x68\x39\x31\x41\x59\x26\x53\x59\xb1\x83\x0f\x2e\x00\x00\x01\xc1\x80\x00\x10\x24\x00\x04\x00\x20\x00\x30\xcd\x34\x21\x9e\xa4\x0c\x2e\xe4\x8a\x70\xa1\x21\x63\x06\x1e\x5c",
        "test_file.json\t[1]\tapplication/x-bzip2; charset=binary",
    ),
    (
        # JSON example: binary data including some plain-text .
        b"\x07\x00\x10\x20\x20\x31",
        "test_file.json\t[1]\tapplication/octet-stream; charset=binary",
    ),
    (
        # Plain-text.
        b"\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64\x21\x0a",
        "test_file.json\t[1]\ttext/plain; charset=unknown",
    ),
    (
        # Whitespace only.
        b"\x0d\x0a\x0d\x0a\x0d\x0a\x0d\x0a\x0d\x0a\x09\x0d",
        "test_file.json\t[1]\ttext/plain; charset=unknown",
    ),
]

integration_testsx = [
    (
        # Plain-text.
        b"\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64\x21\x0a",
        "test_file.json\t[1]\ttext/plain; charset=unknown",
    )
]


@pytest.mark.skipif(
    sys.platform.startswith("win"), reason="python-magic incompatibilties"
)
@pytest.mark.parametrize("data, expected", integration_tests)
@pytest.mark.asyncio
async def test_e2e_output(mocker, data, expected, tmp_path):
    """Integration tests for binary and JSONID output."""
    test_file = tmp_path / "test_file.json"
    test_file.write_bytes(data)
    mocker.patch("src.jsonid.output._format_path", return_value="test_file.json")
    output_patched = mocker.patch("src.jsonid.output.print_result")
    await file_processing.identify_json(
        paths=[test_file],
        strategy=jsonid.decode_strategies,
        binary=True,
        agentout=False,
    )
    output_patched.assert_called()
    output_patched.assert_called_with(expected)


integration_registry = [
    registry_class.RegistryEntry(
        identifier="jrid:0000",
        name=[{"@en": "TEST PAGE 0001"}],
        version="1",
        markers=[
            {"KEY": "values", "ISTYPE": list},
            {"KEY": "hello", "IS": "world"},
            {"KEY": "goodbye", "IS": False},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0001",
        name=[{"@en": "MULTI1"}],
        version="1",
        markers=[
            {"KEY": "data", "ISTYPE": list},
        ],
    ),
    registry_class.RegistryEntry(
        identifier="jrid:0002",
        name=[{"@en": "MULTI2"}],
        version="1",
        markers=[
            {"KEY": "data", "ISTYPE": list},
        ],
    ),
]

TEST_PAGE_JSON: Final[
    str
] = """
{
    "values": [
        1,
        2,
        3.142
    ],
    "hello": "world",
    "goodbye": false
}
"""

TEST_PAGE_YAML: Final[
    str
] = """
---
values:
- 1
- 2
- 3.142
hello: world
goodbye: false
"""

TEST_PAGE_TOML: Final[
    str
] = """
Values = [1, 2, 3.142]
Hello = "world"
Goodbye = false
"""

MULTI_JSON: Final[
    str
] = """
{
    "data": []
}
"""


test_page_tests: Final[list] = [
    (
        integration_registry,
        TEST_PAGE_JSON,
        'test_file.json\t[1]\tapplication/json; charset=UTF-8; doctype="TEST PAGE 0001"; ref=jrid:0000',
    ),
    (
        integration_registry,
        TEST_PAGE_YAML,
        'test_file.json\t[1]\tapplication/yaml; charset=UTF-8; doctype="TEST PAGE 0001"; ref=jrid:0000',
    ),
    (
        integration_registry,
        TEST_PAGE_TOML,
        'test_file.json\t[1]\tapplication/toml; charset=UTF-8; doctype="Tom\'s Obvious, Minimal Language (TOML)"; ref=jrid:TOML',
    ),
    (
        integration_registry,
        MULTI_JSON,
        'test_file.json\t[2]\tapplication/json; charset=UTF-8; doctype="MULTI1"; ref=jrid:0001 | application/json; charset=UTF-8; doctype="MULTI2"; ref=jrid:0002',
    ),
]


@pytest.mark.skipif(
    sys.platform.startswith("win"), reason="python-magic incompatibilties"
)
@pytest.mark.parametrize("registry, data, expected", test_page_tests)
@pytest.mark.asyncio
async def test_integration_with_test_page(mocker, tmp_path, registry, data, expected):
    """Use a placeholder registry to test expected results for
    real-world-ish objects.
    """
    mocker.patch("src.jsonid.registry_data.registry", return_value=registry)
    test_file = tmp_path / "test_file.json"
    test_file.write_bytes(data.strip().encode())
    mocker.patch("src.jsonid.output._format_path", return_value="test_file.json")
    output_patched = mocker.patch("src.jsonid.output.print_result")
    await file_processing.identify_json(
        paths=[test_file],
        strategy=jsonid.decode_strategies,
        binary=False,
        agentout=False,
    )
    output_patched.assert_called()
    output_patched.assert_called_with(expected)

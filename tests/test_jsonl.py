"""JSONL requires some slightly special handling. Let's make sure
any exceptions to the rule work here.
"""

import pytest

from src.jsonid import file_processing, registry

jsonl_1_valid = """
 1
 2
 3
"""
jsonl_2_valid = """
[1]
[2]
[3]
"""
jsonl_3_valid = """
{"hello": "world"}
{"world": "hello"}
"""
jsonl_4_invalid = ""
jsonl_5_not_jsonl = "[1, 2, 3]"

jsonl_tests = [
    (jsonl_1_valid, True, registry.DOCTYPE_JSONL),
    (jsonl_2_valid, True, registry.DOCTYPE_JSONL),
    (jsonl_3_valid, True, registry.DOCTYPE_JSONL),
    (jsonl_4_invalid, False, False),
    (jsonl_5_not_jsonl, False, False),
]


@pytest.mark.parametrize("content, validity, doctype", jsonl_tests)
def test_jsonl_processing(content, validity, doctype):
    """Ensure that JSONL processing worrks as expected."""
    valid, _, doctype_res = file_processing._jsonl_processing(content)
    assert valid == validity
    assert doctype_res == doctype

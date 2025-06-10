"""Proof of concept for other encodings."""

from src.jsonid import file_processing, registry


def test_yaml_only():
    """Ensure that YAML can find its way through the decode process.

    NB. somewhat of a sandbox test so that output can be observed
    quickly.
    """
    only_yaml = """
        ---
        test1: 1
        test2: "data"
    """
    valid, data, doctype = file_processing.decode(
        content=only_yaml.strip(),
        strategy=[registry.DOCTYPE_YAML],
    )
    assert valid is True
    assert data == {"test1": 1, "test2": "data"}
    assert doctype == registry.DOCTYPE_YAML

    only_yaml = """
        ---
        test1: |
          test2: "data"
    """
    valid, data, doctype = file_processing.decode(
        only_yaml.strip(),
        strategy=[registry.DOCTYPE_YAML],
    )
    assert valid is True
    assert data == {"test1": 'test2: "data"'}
    assert doctype == registry.DOCTYPE_YAML

    only_yaml = """
        ---
        test1: [1, 2, 3]
    """
    valid, data, doctype = file_processing.decode(
        only_yaml.strip(),
        strategy=[registry.DOCTYPE_YAML],
    )
    assert valid is True
    assert data == {"test1": [1, 2, 3]}
    assert doctype == registry.DOCTYPE_YAML


def test_toml_only():
    """Ensure that TOML can find its way through the decode process.

    NB. somewhat of a sandbox test so that output can be observed
    quickly.
    """

    only_toml = """
    test1 = 1
    test2 = "data"
    """
    valid, data, doctype = file_processing.decode(
        only_toml,
        strategy=[registry.DOCTYPE_TOML],
    )
    assert valid is True
    assert data == {"test1": 1, "test2": "data"}
    assert doctype == registry.DOCTYPE_TOML

    only_toml = """
    [[list0]]
    test1 = 1
    test2 = "data"
    """
    valid, data, doctype = file_processing.decode(
        only_toml,
        strategy=[registry.DOCTYPE_TOML],
    )
    assert valid is True
    assert data == {"list0": [{"test1": 1, "test2": "data"}]}
    assert doctype == registry.DOCTYPE_TOML

    only_toml = """
    test0 = 1
    [[list0]]
    test1 = 1
    test2 = "data"
    """
    valid, data, doctype = file_processing.decode(
        only_toml,
        strategy=[registry.DOCTYPE_TOML],
    )
    assert valid is True
    assert data == {"test0": 1, "list0": [{"test1": 1, "test2": "data"}]}
    assert doctype == registry.DOCTYPE_TOML

    only_toml = """
    [nested0]
    test1 = 1
    test2 = "data"
    """
    valid, data, doctype = file_processing.decode(
        only_toml,
        strategy=[registry.DOCTYPE_TOML],
    )
    assert valid is True
    assert data == {"nested0": {"test1": 1, "test2": "data"}}
    assert doctype == registry.DOCTYPE_TOML

    only_toml = """
    test1 = [1, 2, 3]
    """
    valid, data, doctype = file_processing.decode(
        only_toml,
        strategy=[registry.DOCTYPE_TOML],
    )
    assert valid is True
    assert data == {"test1": [1, 2, 3]}
    assert doctype == registry.DOCTYPE_TOML

"""Standard objects to be returned by JSONID for consistency.

For the future, map these correctly to the MIMETypes that they are
expected to return as when output to the CLI.
"""

import logging

try:
    import registry
except ModuleNotFoundError:
    try:
        from src.jsonid import registry
    except ModuleNotFoundError:
        from jsonid import registry


logger = logging.getLogger(__name__)


def no_id_binary() -> registry.BaseCharacteristics:
    """Base object for a binary object we can't identify."""
    return registry.BaseCharacteristics(
        binary=True,
    )


def no_id_compression(compression: str) -> registry.BaseCharacteristics:
    """Base object for a compressed file that we can't identify."""
    return registry.BaseCharacteristics(
        binary=True,
        compression=compression,
    )


def no_id_text() -> registry.BaseCharacteristics:
    """Base object for a text file we can't identify."""
    return registry.BaseCharacteristics(
        text=True,
    )


def no_id_whitespace() -> registry.BaseCharacteristics:
    """Base object when we just have whitespace."""
    return registry.BaseCharacteristics(
        text=True,
        only_whitespace=True,
    )


def no_id_empty() -> registry.BaseCharacteristics:
    """Base object for an empty file."""
    return registry.BaseCharacteristics(
        empty=True,
    )


def possible_id(content: bytes, compression: str) -> registry.BaseCharacteristics:
    """Base object when we have a possible identification."""
    return registry.BaseCharacteristics(
        data=content,
        compression=compression,
        text=True,
    )

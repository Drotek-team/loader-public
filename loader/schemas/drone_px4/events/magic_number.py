from enum import IntEnum


class MagicNumber(IntEnum):
    """The magic number to identify the version of the schema."""

    old = 0xAA55
    new = 0xAA66

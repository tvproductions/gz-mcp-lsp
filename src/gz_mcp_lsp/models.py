"""Small immutable values shared across adapter boundaries."""

import os
from dataclasses import dataclass

type Json = bool | int | float | str | list[Json] | dict[str, Json] | None
type Result = dict[str, Json]
type TransactionReceipt = dict[str, Json]


class AdapterError(Exception):
    """A deliberate domain failure with source-free structured details."""

    def __init__(
        self,
        code: str,
        message: str,
        retryable: bool = False,
        details: dict[str, Json] | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable
        self.details = details or {}


@dataclass(frozen=True, slots=True)
class Position:
    """Zero-based line and UTF-16 code-unit character."""

    line: int
    character: int

    def __post_init__(self):
        if any(type(value) is not int or value < 0 for value in (self.line, self.character)):
            raise AdapterError("INVALID_INPUT", "Position requires nonnegative integers")


@dataclass(frozen=True, slots=True)
class Range:
    """An ordered, end-exclusive source range."""

    start: Position
    end: Position

    def __post_init__(self):
        if not isinstance(self.start, Position) or not isinstance(self.end, Position):
            raise AdapterError("INVALID_INPUT", "Range requires positions")
        if (self.end.line, self.end.character) < (self.start.line, self.start.character):
            raise AdapterError("INVALID_INPUT", "Range end precedes its start")


@dataclass(frozen=True, slots=True)
class TextEdit:
    """Replace the original snapshot's range with explicit text."""

    range: Range
    new_text: str

    def __post_init__(self):
        if not isinstance(self.range, Range) or not isinstance(self.new_text, str):
            raise AdapterError("INVALID_INPUT", "Text edit requires a range and text")


@dataclass(frozen=True, slots=True)
class FileIdentity:
    """Filesystem identity and mode, independent of source coordinates."""

    device: int
    inode: int
    mode: int
    links: int

    @classmethod
    def from_stat(cls, value: os.stat_result) -> FileIdentity:
        """Capture only identity fields needed at filesystem boundaries."""
        return cls(value.st_dev, value.st_ino, value.st_mode, value.st_nlink)


@dataclass(frozen=True, slots=True)
class Snapshot:
    """Exact saved bytes and the identity observed while reading."""

    uri: str
    data: bytes
    sha256: str
    version: int
    identity: FileIdentity

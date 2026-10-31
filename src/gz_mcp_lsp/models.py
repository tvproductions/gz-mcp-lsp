"""Protocol-independent values shared by the adapter boundaries."""

from dataclasses import dataclass

type Json = bool | int | float | str | list[Json] | dict[str, Json] | None
type Result = dict[str, Json]


class AdapterError(Exception):
    """A stable operation failure, distinct from an empty semantic result."""

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


@dataclass(frozen=True, order=True)
class Position:
    """Zero-based LSP UTF-16 code-unit position."""

    line: int
    character: int

    def __post_init__(self):
        if any(type(value) is not int or value < 0 for value in (self.line, self.character)):
            raise AdapterError("INVALID_INPUT", "Positions require nonnegative integers")


@dataclass(frozen=True)
class Range:
    """End-exclusive positions referring to one immutable document snapshot."""

    start: Position
    end: Position

    def __post_init__(self):
        if self.end < self.start:
            raise AdapterError("INVALID_INPUT", "Range end precedes start")


@dataclass(frozen=True)
class TextEdit:
    """A replacement relative to the original snapshot, never to prior edits."""

    range: Range
    new_text: str


@dataclass(frozen=True)
class FileIdentity:
    """Filesystem object identity used for authorization and conflict checks."""

    device: int
    inode: int
    mode: int
    links: int
    owner: int = -1
    group: int = -1


@dataclass(frozen=True)
class Snapshot:
    """Exact saved document bytes and their synchronization identity."""

    uri: str
    data: bytes
    sha256: str
    version: int
    identity: FileIdentity
    parents: tuple[FileIdentity, ...] = ()

"""Current pull diagnostics with bounded identity-bound resultId caching."""

import copy
import json
from collections import OrderedDict
from dataclasses import dataclass
from typing import cast

from gz_mcp_lsp.documents import Documents, GenerationContext, _owned_io
from gz_mcp_lsp.models import AdapterError, Json, Result, Snapshot
from gz_mcp_lsp.results import bounded, encoded_size, envelope, provenance
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.source_text import parse_range, range_json, source_context


@dataclass(frozen=True, slots=True)
class _Cached:
    generation: str
    sha256: str
    result_id: str | None
    items: list[Json]


class Diagnostics:
    """Never replace a failed pull or unmatched unchanged report with an empty list."""

    def __init__(self, documents: Documents, session: Session):
        self.documents = documents
        self.session = session
        self._generation = ""
        self._cache: OrderedDict[str, _Cached] = OrderedDict()

    async def diagnostics(self, uri: str, context_lines: int = 0) -> Result:
        if type(context_lines) is not int or not 0 <= context_lines <= 20:
            raise AdapterError(
                "INVALID_INPUT", "context_lines must be an integer from zero through twenty"
            )
        pending: dict[str, _Cached] = {}
        async with self.documents.read(uri) as read:
            context = GenerationContext(read.generation, read.rpc)
            provider = self.session.capabilities.get("diagnosticProvider")
            if not isinstance(provider, dict):
                raise AdapterError(
                    "UNSUPPORTED", "Language server does not advertise pull diagnostics"
                )
            if self._generation != context.generation:
                self._cache.clear()
                self._generation = context.generation
            key = await _owned_io(self.documents.workspace.canonical_uri, uri)
            prior = self._cache.get(key)
            params: dict[str, Json] = {"textDocument": {"uri": uri}}
            if "identifier" in provider:
                if not isinstance(provider["identifier"], str):
                    raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic provider identifier")
                params["identifier"] = provider["identifier"]
            if (
                self._matches(prior, context, read.snapshot)
                and prior is not None
                and prior.result_id is not None
            ):
                params["previousResultId"] = prior.result_id
            report = await context.rpc.request(
                "textDocument/diagnostic",
                params,
                timeout=self.documents.workspace.config.request_timeout_seconds,
            )
            items, result_id = await self._report(report, uri, read.snapshot, context, pending)
            documents = {uri: provenance(read.snapshot)}
            displayed = await self._context(items, read.snapshot, context, context_lines, documents)
            related = await self._related(report, context, context_lines, documents, pending)
            result: dict[str, Json] = {
                "items": displayed,
                "result_id": result_id,
                "related_documents": related,
            }
            value = envelope(
                "diagnostics",
                context.generation,
                result,
                documents,
                self.documents.workspace.config.limits.result_bytes,
            )
        # Final manifest validation has succeeded; failed/stale operations never populate cache.
        for key, entry in pending.items():
            self._cache[key] = entry
            self._cache.move_to_end(key)
        while len(self._cache) > self.documents.workspace.config.limits.in_flight_reads:
            self._cache.popitem(last=False)
        return value

    @staticmethod
    def _matches(entry: _Cached | None, context: GenerationContext, snapshot: Snapshot) -> bool:
        return (
            entry is not None
            and entry.generation == context.generation
            and entry.sha256 == snapshot.sha256
        )

    async def _report(
        self,
        report: Json,
        uri: str,
        snapshot: Snapshot | None,
        context: GenerationContext,
        pending: dict[str, _Cached],
    ) -> tuple[list[Json], str | None]:
        if not isinstance(report, dict):
            raise AdapterError("PROTOCOL_ERROR", "Invalid document diagnostic report")
        result_id = report.get("resultId")
        if result_id is not None and not isinstance(result_id, str):
            raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic resultId")
        key = (
            await _owned_io(self.documents.workspace.canonical_uri, uri)
            if snapshot is not None
            else None
        )
        prior = self._cache.get(key) if key is not None else None
        kind = report.get("kind")
        if kind == "unchanged":
            if (
                snapshot is None
                or result_id is None
                or prior is None
                or not self._matches(prior, context, snapshot)
                or prior.result_id != result_id
            ):
                raise AdapterError(
                    "PROTOCOL_ERROR", "Unchanged diagnostics have no matching saved identity"
                )
            items = copy.deepcopy(prior.items)
            for item in items:
                cast("dict[str, Json]", item)["uri"] = uri
        elif kind == "full":
            raw = report.get("items")
            if not isinstance(raw, list):
                raise AdapterError("PROTOCOL_ERROR", "Full diagnostic report requires items")
            items = await self._items(raw, uri, snapshot)
        else:
            raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic report kind")
        bounded(items, self.documents.workspace.config.limits.result_bytes)
        if key is not None and snapshot is not None:
            pending[key] = _Cached(
                context.generation, snapshot.sha256, result_id, copy.deepcopy(items)
            )
        return items, result_id

    async def _items(self, raw: list[Json], uri: str, snapshot: Snapshot | None) -> list[Json]:
        items: list[Json] = []
        used = 0
        for diagnostic in raw:
            if not isinstance(diagnostic, dict) or not isinstance(diagnostic.get("message"), str):
                raise AdapterError("PROTOCOL_ERROR", "Diagnostic requires a message")
            extent = parse_range(diagnostic.get("range"))
            if snapshot is not None:
                try:
                    self.documents.workspace.offset(snapshot, extent.start)
                    self.documents.workspace.offset(snapshot, extent.end)
                except AdapterError as error:
                    raise AdapterError(
                        "PROTOCOL_ERROR", "Diagnostic range exceeds saved source"
                    ) from error
            item: dict[str, Json] = {
                "uri": uri,
                "range": range_json(extent),
                "message": diagnostic["message"],
            }
            self._fields(diagnostic, item)
            if "relatedInformation" in diagnostic:
                related = diagnostic["relatedInformation"]
                if not isinstance(related, list):
                    raise AdapterError("PROTOCOL_ERROR", "Invalid related diagnostic information")
                information: list[Json] = []
                for value in related:
                    information.append(await self._information(value))
                item["related_information"] = sorted(
                    information,
                    key=lambda value: json.dumps(value, sort_keys=True, ensure_ascii=False),
                )
            used += encoded_size(item)
            if used > self.documents.workspace.config.limits.result_bytes:
                raise AdapterError("RESULT_LIMIT", "Diagnostic list exceeds its byte budget")
            items.append(item)
        return sorted(items, key=lambda value: _diagnostic_key(cast("dict[str, Json]", value)))

    @staticmethod
    def _fields(raw: dict[str, Json], item: dict[str, Json]) -> None:
        if "severity" in raw:
            severity = raw["severity"]
            if type(severity) is not int or severity not in (1, 2, 3, 4):
                raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic severity")
            item["severity"] = severity
        if "code" in raw:
            code = raw["code"]
            if type(code) not in (int, str):
                raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic code")
            item["code"] = code
        if "source" in raw:
            if not isinstance(raw["source"], str):
                raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic source")
            item["source"] = raw["source"]
        if "tags" in raw:
            tags = raw["tags"]
            if not isinstance(tags, list) or any(type(tag) is not int for tag in tags):
                raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic tags")
            item["tags"] = tags
        if "codeDescription" in raw:
            description = raw["codeDescription"]
            if not isinstance(description, dict) or not isinstance(description.get("href"), str):
                raise AdapterError("PROTOCOL_ERROR", "Invalid diagnostic code description")
            item["code_description"] = {"href": description["href"]}
        # Opaque code-action data is not requested or exposed; code actions are out of scope.

    async def _information(self, raw: Json) -> Json:
        if not isinstance(raw, dict) or not isinstance(raw.get("message"), str):
            raise AdapterError("PROTOCOL_ERROR", "Invalid related diagnostic message")
        location = raw.get("location")
        if not isinstance(location, dict) or not isinstance(location.get("uri"), str):
            raise AdapterError("PROTOCOL_ERROR", "Invalid related diagnostic location")
        uri = location["uri"]
        scope = await _owned_io(self.documents.workspace.source_scope, uri)
        return {
            "uri": uri,
            "range": range_json(parse_range(location.get("range"))),
            "message": raw["message"],
            "source_scope": scope,
        }

    async def _context(
        self,
        base: list[Json],
        snapshot: Snapshot,
        context: GenerationContext,
        lines: int,
        documents: dict[str, Json],
    ) -> list[Json]:
        items = copy.deepcopy(base)
        if not lines:
            return items
        used = 0
        for value in items:
            item = cast("dict[str, Json]", value)
            item["context"] = source_context(snapshot, parse_range(item["range"]), lines)
            bounded(item, self.documents.workspace.config.limits.result_bytes)
            information = item.get("related_information", [])
            for entry in cast("list[Json]", information):
                related = cast("dict[str, Json]", entry)
                if related["source_scope"] != "workspace":
                    continue
                uri = cast("str", related["uri"])
                async with self.documents.document(context, uri) as target:
                    related["context"] = source_context(
                        target, parse_range(related["range"]), lines
                    )
                    documents[uri] = provenance(target)
                    bounded(item, self.documents.workspace.config.limits.result_bytes)
            used += encoded_size(item)
            if used > self.documents.workspace.config.limits.result_bytes:
                raise AdapterError("RESULT_LIMIT", "Diagnostic context exceeds its byte budget")
        bounded(items, self.documents.workspace.config.limits.result_bytes)
        return items

    async def _related(
        self,
        report: Json,
        context: GenerationContext,
        lines: int,
        documents: dict[str, Json],
        pending: dict[str, _Cached],
    ) -> list[Json]:
        assert isinstance(report, dict)
        raw = report.get("relatedDocuments", {})
        if not isinstance(raw, dict):
            raise AdapterError("PROTOCOL_ERROR", "Invalid related document reports")
        related: list[Json] = []
        used = 0
        for uri, document_report in sorted(raw.items()):
            scope = await _owned_io(self.documents.workspace.source_scope, uri)
            if scope == "workspace":
                async with self.documents.document(context, uri) as target:
                    items, result_id = await self._report(
                        document_report, uri, target, context, pending
                    )
                    items = await self._context(items, target, context, lines, documents)
                    documents[uri] = provenance(target)
            elif scope == "external":
                items, result_id = await self._report(document_report, uri, None, context, pending)
            else:
                raise AdapterError("SOURCE_UNAVAILABLE", "Related diagnostic source is unavailable")
            value: Json = {
                "uri": uri,
                "source_scope": scope,
                "items": items,
                "result_id": result_id,
            }
            used += encoded_size(value)
            if used > self.documents.workspace.config.limits.result_bytes:
                raise AdapterError("RESULT_LIMIT", "Related diagnostics exceed their byte budget")
            related.append(value)
        return related


def _diagnostic_key(item: dict[str, Json]) -> tuple:
    extent = parse_range(item["range"])
    return (
        item["uri"],
        extent.start.line,
        extent.start.character,
        extent.end.line,
        extent.end.character,
        json.dumps(item, sort_keys=True, ensure_ascii=False),
    )

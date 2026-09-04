#!/usr/bin/env python3
"""Validate Starlight Horizon dataset JSONL against schema + contribution rules.

Zero third-party deps. Exit 0 when every entries/**/*.jsonl line is valid.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

REQUIRED = ("id", "wish", "context", "author", "createdAt")
SECRET_KEYS = {
    "api_key",
    "apikey",
    "password",
    "token",
    "secret",
    "private_key",
    "authorization",
    "access_token",
}
DESTRUCTIVE = re.compile(
    r"\b(destroy|exterminate|enslave|genocide|murder|wipe out|kill (all|every)|harm humans)\b",
    re.IGNORECASE,
)
ISO = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
ID_OK = re.compile(r"^horizon_[A-Za-z0-9_-]+$")
PROVENANCE_CUTOVER = datetime.fromisoformat("2026-09-04T00:00:00+00:00")
PROVENANCE = {
    "historical-source-claim",
    "scholarly-interpretation",
    "starlight-interpretation",
    "original-starlight-philosophy",
    "original-literary-mythic-material",
    "arcanea-fiction",
}
SOURCED = {"historical-source-claim", "scholarly-interpretation"}
FICTIONAL = {"original-literary-mythic-material", "arcanea-fiction"}
ONTOLOGY_DRIFT = re.compile(
    r"\b(Starlight is (?:God|The Source|Lumina)|Lumina is Starlight|"
    r"Shinkami is God|The Tao is The Source|all religions teach Starlight|"
    r"Kunlun was actually Arcanea|quantum physics proves (?:manifestation|spiritual doctrine))\b",
    re.IGNORECASE,
)


class ValidationError(ValueError):
    pass


def _nonempty_str(record: dict, key: str, source: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{source}: '{key}' must be a non-empty string")
    return value.strip()


def validate_record(record: dict, source: str = "record") -> None:
    if not isinstance(record, dict):
        raise ValidationError(f"{source}: record must be a JSON object")

    secret = [k for k in record if k.lower() in SECRET_KEYS]
    if secret:
        raise ValidationError(f"{source}: forbidden field(s) {secret}")

    missing = [k for k in REQUIRED if k not in record]
    if missing:
        raise ValidationError(f"{source}: missing {missing}")

    ident = _nonempty_str(record, "id", source)
    if not ID_OK.match(ident):
        raise ValidationError(
            f"{source}: id must match horizon_<slug> (got {ident!r})"
        )

    wish = _nonempty_str(record, "wish", source)
    if len(wish) < 24:
        raise ValidationError(f"{source}: wish is too thin — be specific")
    if DESTRUCTIVE.search(wish):
        raise ValidationError(f"{source}: wish must be constructive")

    _nonempty_str(record, "context", source)
    _nonempty_str(record, "author", source)

    created = _nonempty_str(record, "createdAt", source)
    if not ISO.match(created):
        raise ValidationError(f"{source}: createdAt must be ISO-8601 (got {created!r})")
    try:
        created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"{source}: createdAt not parseable") from exc

    combined_text = f"{wish} {record.get('context', '')}"
    if ONTOLOGY_DRIFT.search(combined_text):
        raise ValidationError(f"{source}: ontology/provenance boundary violation")

    provenance = record.get("provenance")
    if created_dt >= PROVENANCE_CUTOVER and provenance not in PROVENANCE:
        raise ValidationError(f"{source}: provenance is required for post-cutover records")
    if provenance is not None and provenance not in PROVENANCE:
        raise ValidationError(f"{source}: unknown provenance class {provenance!r}")
    if provenance in SOURCED:
        source_ids = record.get("sourceIds")
        if not isinstance(source_ids, list) or not source_ids or not all(
            isinstance(item, str) and item.strip() for item in source_ids
        ):
            raise ValidationError(f"{source}: sourced claims require non-empty sourceIds")
    if provenance in FICTIONAL:
        _nonempty_str(record, "fictionBoundary", source)

    if "coAuthored" in record and not isinstance(record["coAuthored"], bool):
        raise ValidationError(f"{source}: coAuthored must be a boolean")

    if "tags" in record:
        tags = record["tags"]
        if not isinstance(tags, list) or not all(isinstance(t, str) and t.strip() for t in tags):
            raise ValidationError(f"{source}: tags must be an array of non-empty strings")


def validate_dataset(root: Path) -> list[str]:
    errors: list[str] = []
    entries = root / "entries"
    if not entries.is_dir():
        return [f"{entries}: missing entries/ directory"]

    seen: dict[str, str] = {}
    files = sorted(entries.glob("**/*.jsonl"))
    if not files:
        return [f"{entries}: no .jsonl files"]

    for path in files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        if not text.strip():
            errors.append(f"{rel}: empty file")
            continue
        for index, raw in enumerate(text.splitlines(), start=1):
            if not raw.strip():
                continue
            source = f"{rel}:{index}"
            try:
                record = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{source}: invalid JSON ({exc.msg})")
                continue
            try:
                validate_record(record, source=source)
            except ValidationError as exc:
                errors.append(str(exc))
                continue
            ident = record["id"]
            if ident in seen:
                errors.append(f"{source}: duplicate id {ident!r} (also {seen[ident]})")
            else:
                seen[ident] = source
    return errors


def main(argv: list[str] | None = None) -> int:
    root = Path(argv[1]).resolve() if argv and len(argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate_dataset(root)
    if errors:
        print(f"Horizon dataset invalid ({len(errors)} error(s)):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("Horizon dataset valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

"""Tests for the Horizon dataset JSONL validator."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate import ValidationError, validate_dataset, validate_record  # noqa: E402


VALID = {
    "id": "horizon_1708891234_abc123",
    "wish": "That every creator owns the memory of their own mind",
    "context": "Written after realizing platform lock-in is memory lock-in",
    "author": "example",
    "coAuthored": True,
    "tags": ["sovereignty", "memory"],
    "createdAt": "2026-08-18T00:00:00Z",
}


class ValidateRecordTests(unittest.TestCase):
    def test_valid_record_passes(self) -> None:
        validate_record(VALID, source="test")

    def test_missing_wish_fails(self) -> None:
        bad = dict(VALID)
        del bad["wish"]
        with self.assertRaises(ValidationError):
            validate_record(bad, source="test")

    def test_empty_wish_fails(self) -> None:
        bad = dict(VALID, wish="   ")
        with self.assertRaises(ValidationError):
            validate_record(bad, source="test")

    def test_destructive_wish_fails(self) -> None:
        bad = dict(VALID, wish="That we destroy all competing civilizations")
        with self.assertRaises(ValidationError):
            validate_record(bad, source="test")

    def test_invalid_created_at_fails(self) -> None:
        bad = dict(VALID, createdAt="yesterday")
        with self.assertRaises(ValidationError):
            validate_record(bad, source="test")

    def test_tags_must_be_strings(self) -> None:
        bad = dict(VALID, tags=["ok", 12])
        with self.assertRaises(ValidationError):
            validate_record(bad, source="test")

    def test_secret_field_fails(self) -> None:
        bad = dict(VALID, api_key="sk-not-a-real-key-but-blocked")
        with self.assertRaises(ValidationError):
            validate_record(bad, source="test")

    def test_post_cutover_record_requires_provenance(self) -> None:
        bad = dict(VALID, createdAt="2026-09-04T00:00:00Z")
        with self.assertRaises(ValidationError):
            validate_record(bad, source="test")

    def test_sourced_claim_requires_source_ids(self) -> None:
        bad = dict(
            VALID,
            createdAt="2026-09-04T00:00:00Z",
            provenance="scholarly-interpretation",
        )
        with self.assertRaises(ValidationError):
            validate_record(bad, source="test")

    def test_fiction_requires_boundary(self) -> None:
        bad = dict(
            VALID,
            createdAt="2026-09-04T00:00:00Z",
            provenance="arcanea-fiction",
        )
        with self.assertRaises(ValidationError):
            validate_record(bad, source="test")

    def test_valid_post_cutover_record_passes(self) -> None:
        record = dict(
            VALID,
            createdAt="2026-09-04T00:00:00Z",
            provenance="original-starlight-philosophy",
            sourceIds=[],
        )
        validate_record(record, source="test")


class ValidateDatasetTests(unittest.TestCase):
    def test_repo_entries_pass(self) -> None:
        errors = validate_dataset(ROOT)
        self.assertEqual(errors, [])

    def test_duplicate_ids_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            month = root / "entries" / "2026-08"
            month.mkdir(parents=True)
            line = json.dumps(VALID)
            (month / "2026-08.jsonl").write_text(line + "\n" + line + "\n", encoding="utf-8")
            (root / "schema.json").write_text(
                (ROOT / "schema.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            errors = validate_dataset(root)
            self.assertTrue(any("duplicate" in e.lower() for e in errors), errors)

    def test_invalid_json_line_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            month = root / "entries" / "2026-08"
            month.mkdir(parents=True)
            (month / "2026-08.jsonl").write_text("{not json}\n", encoding="utf-8")
            (root / "schema.json").write_text("{}", encoding="utf-8")
            errors = validate_dataset(root)
            self.assertTrue(any("json" in e.lower() for e in errors), errors)


if __name__ == "__main__":
    unittest.main()

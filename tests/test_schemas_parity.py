#!/usr/bin/env python3
"""
Parity tests between references/schemas.md (Markdown fallback source) and
references/schemas/*.json (standalone machine-readable authority).

The standalone JSON files are the authority; the Markdown blocks exist only as
a degradation path when the JSON files are unavailable. Any single-sided edit
(two-source drift) fails here.
"""

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "codex-doc-first-development"
REFERENCES = SKILL_ROOT / "references"
SCHEMAS_MD = REFERENCES / "schemas.md"
SCHEMAS_DIR = REFERENCES / "schemas"


def extract_markdown_schemas(content: str) -> dict:
    """Extract {schema_id: dict} from schemas.md `// schema-id:` anchored blocks."""
    schemas = {}
    for match in re.finditer(r"// schema-id:\s*(\w+)", content):
        schema_id = match.group(1)
        json_start = content.find("{", match.end())
        if json_start == -1:
            continue
        brace_count = 0
        json_end = -1
        for i in range(json_start, len(content)):
            if content[i] == "{":
                brace_count += 1
            elif content[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    json_end = i + 1
                    break
        if json_end == -1:
            continue
        schemas[schema_id] = json.loads(content[json_start:json_end])
    return schemas


class TestSchemaParity(unittest.TestCase):
    def setUp(self):
        self.markdown_schemas = extract_markdown_schemas(SCHEMAS_MD.read_text(encoding="utf-8"))
        self.json_schemas = {
            p.stem: json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(SCHEMAS_DIR.glob("*.json"))
        }

    def test_every_standalone_json_has_markdown_block(self):
        for schema_id in self.json_schemas:
            self.assertIn(schema_id, self.markdown_schemas, f"{schema_id}.json missing from schemas.md")

    def test_every_markdown_block_has_standalone_json(self):
        for schema_id in self.markdown_schemas:
            self.assertIn(schema_id, self.json_schemas, f"schemas.md block {schema_id} has no standalone JSON")

    def test_markdown_blocks_match_standalone_json(self):
        for schema_id, json_schema in self.json_schemas.items():
            self.assertEqual(
                self.markdown_schemas.get(schema_id),
                json_schema,
                f"{schema_id} drifted between schemas.md and schemas/{schema_id}.json",
            )

    def test_artifact_metadata_declared_in_both_sources(self):
        # The optional artifact_metadata property must exist in BOTH sources so
        # the Markdown degradation path accepts the same records as the JSON path.
        for schema_id in ("ExecutionTraceSchema", "AuditLogSchema"):
            for source, schemas in (("json", self.json_schemas), ("markdown", self.markdown_schemas)):
                props = schemas[schema_id]["properties"]
                self.assertIn("artifact_metadata", props, f"{schema_id} missing artifact_metadata in {source}")


if __name__ == "__main__":
    unittest.main()

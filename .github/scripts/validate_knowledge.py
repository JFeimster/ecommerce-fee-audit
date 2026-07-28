from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / "knowledge"
errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: JSON error: {exc}")
        return None


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: YAML error: {exc}")
        return None


def load_front_matter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, re.DOTALL)
    if not match:
        return None
    try:
        metadata = yaml.safe_load(match.group(1))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: front-matter YAML error: {exc}")
        return None
    if metadata is None:
        return {}
    if not isinstance(metadata, dict):
        fail(f"{path.relative_to(ROOT)}: front matter must be a mapping")
        return None
    return metadata


def related_file_exists(source_path: Path, reference: str) -> bool:
    if Path(reference).is_absolute():
        return False
    candidates = (source_path.parent / reference, KNOWLEDGE / reference)
    return any(candidate.resolve().is_file() for candidate in candidates)


for path in KNOWLEDGE.rglob("*.json"):
    load_json(path)

for path in KNOWLEDGE.rglob("*.yaml"):
    load_yaml(path)
for path in KNOWLEDGE.rglob("*.yml"):
    load_yaml(path)

for path in KNOWLEDGE.rglob("*.csv"):
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.reader(handle))
        if rows:
            width = len(rows[0])
            bad = [index + 1 for index, row in enumerate(rows) if len(row) != width]
            if bad:
                fail(f"{path.relative_to(ROOT)}: inconsistent CSV widths on rows {bad}")
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: CSV error: {exc}")

for schema_name in ("master-transaction-schema.json", "output-schema.json"):
    path = KNOWLEDGE / schema_name
    if not path.exists():
        fail(f"Missing canonical schema: {path.relative_to(ROOT)}")
        continue
    schema = load_json(path)
    if schema is None:
        continue
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for index, example in enumerate(schema.get("examples", []), start=1):
            found = list(validator.iter_errors(example))
            if found:
                fail(f"{schema_name} example {index}: {found[0].message}")
    except Exception as exc:
        fail(f"{schema_name}: schema validation error: {exc}")

instruction_path = KNOWLEDGE / "ai-platform-fee-audit-copilot-builder-instructions.md"
if instruction_path.exists():
    text = instruction_path.read_text(encoding="utf-8")
    marker = "## Builder-Ready Instructions"
    if marker in text:
        section = text.split(marker, 1)[1].split("\n---\n", 1)[0].strip()
        section = "\n".join(line for line in section.splitlines() if not line.lstrip().startswith(">"))
        if len(section) > 8000:
            fail(f"Builder-ready instructions exceed 8,000 characters: {len(section)}")

for path in KNOWLEDGE.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    metadata = load_front_matter(path)
    if metadata and "related_files" in metadata:
        related_files = metadata["related_files"]
        if not isinstance(related_files, list) or not all(isinstance(item, str) for item in related_files):
            fail(f"{path.relative_to(ROOT)}: related_files must be a list of paths")
        else:
            for reference in related_files:
                if not related_file_exists(path, reference):
                    fail(f"{path.relative_to(ROOT)}: related_files target does not exist: {reference}")
    if re.search(r"(?i)(sk-[a-z0-9]{20,}|api[_-]?key\s*[:=]\s*\S+|password\s*[:=]\s*\S+)", text):
        fail(f"{path.relative_to(ROOT)}: possible credential pattern")

if errors:
    print("Knowledge integrity validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Knowledge integrity validation passed.")

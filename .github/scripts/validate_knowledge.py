from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from jsonschema import FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / "knowledge"
API_SCHEMAS = ROOT / "api" / "schemas"
PRODUCT_CATALOG = ROOT / "config" / "products" / "product-catalog.yaml"
BATCH_TWO_SCHEMAS = (
    "audit-intake.schema.json",
    "audit-job.schema.json",
    "audit-source.schema.json",
    "audit-finding.schema.json",
    "event-envelope.schema.json",
    "connector-config.schema.json",
    "product-entitlement.schema.json",
    "export-request.schema.json",
    "upload-session.schema.json",
    "user-consent.schema.json",
    "audit-period.schema.json",
    "service-order.schema.json",
)
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


def nested_values(value, key: str):
    if isinstance(value, dict):
        if key in value:
            yield value[key]
        for child in value.values():
            yield from nested_values(child, key)
    elif isinstance(value, list):
        for child in value:
            yield from nested_values(child, key)


def contains_sensitive_example_value(value) -> bool:
    sensitive_key = re.compile(r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token|secret|password|credential|ssn|bank[_-]?account)")
    sensitive_value = re.compile(r"(?i)(sk-[a-z0-9]{20,}|akia[0-9a-z]{16}|-----begin (?:rsa )?private key-----)")
    if isinstance(value, dict):
        return any(sensitive_key.search(str(key)) or contains_sensitive_example_value(item) for key, item in value.items())
    if isinstance(value, list):
        return any(contains_sensitive_example_value(item) for item in value)
    return isinstance(value, str) and bool(sensitive_value.search(value))


def validate_batch_two_schemas() -> None:
    catalog = load_yaml(PRODUCT_CATALOG)
    if not isinstance(catalog, dict):
        fail(f"Missing or invalid canonical product catalog: {PRODUCT_CATALOG.relative_to(ROOT)}")
        return
    product_ids = {item.get("product_id") for item in catalog.get("products", []) if isinstance(item, dict)}
    if len(product_ids) != 10 or None in product_ids:
        fail("config/products/product-catalog.yaml: expected 10 canonical product IDs")

    schemas: list[tuple[Path, dict]] = []
    ids: set[str] = set()
    required_keys = {"$schema", "$id", "title", "description", "type", "required", "additionalProperties", "examples", "x-value-semantics"}
    required_semantics = {"null", "zero", "omitted", "currency", "percentage"}
    for filename in BATCH_TWO_SCHEMAS:
        path = API_SCHEMAS / filename
        if not path.exists():
            fail(f"Missing Batch 2 schema: {path.relative_to(ROOT)}")
            continue
        schema = load_json(path)
        if not isinstance(schema, dict):
            continue
        missing_keys = required_keys - schema.keys()
        if missing_keys:
            fail(f"{path.relative_to(ROOT)}: missing required schema keys {sorted(missing_keys)}")
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            fail(f"{path.relative_to(ROOT)}: must declare JSON Schema Draft 2020-12")
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            fail(f"{path.relative_to(ROOT)}: missing stable $id")
        elif schema_id in ids:
            fail(f"Duplicate Batch 2 schema $id: {schema_id}")
        else:
            ids.add(schema_id)
        semantics = schema.get("x-value-semantics")
        if not isinstance(semantics, dict) or not required_semantics.issubset(semantics):
            fail(f"{path.relative_to(ROOT)}: x-value-semantics must define null, zero, omitted, currency, and percentage")
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            fail(f"{path.relative_to(ROOT)}: Draft 2020-12 schema error: {exc}")
        schemas.append((path, schema))

    registry = Registry()
    for _, schema in schemas:
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            registry = registry.with_resource(schema_id, Resource.from_contents(schema))

    for path, schema in schemas:
        for reference in nested_values(schema, "$ref"):
            if not isinstance(reference, str) or reference.startswith("#"):
                continue
            if "://" in reference:
                fail(f"{path.relative_to(ROOT)}: external $ref is not permitted: {reference}")
                continue
            target = (path.parent / reference.split("#", 1)[0]).resolve()
            if not target.is_file():
                fail(f"{path.relative_to(ROOT)}: unresolved relative $ref: {reference}")
        for enum in nested_values(schema, "enum"):
            if isinstance(enum, list) and set(enum) & product_ids and set(enum) != product_ids:
                fail(f"{path.relative_to(ROOT)}: product ID enum does not match the canonical catalog")
        for enum in nested_values(schema, "enum"):
            if isinstance(enum, list):
                statuses = [value for value in enum if isinstance(value, str) and value in {"draft", "open", "closed", "archived", "submitted", "accepted", "declined", "queued", "running", "succeeded", "failed", "cancelled", "blocked", "pending", "granted", "expired", "revoked", "unreviewed", "reviewed", "approved", "rejected", "escalated", "active", "suspended", "ready", "generating", "requested", "completed", "connected", "disabled", "error", "unsupported", "not_configured", "pending_consent", "processing", "available", "unusable", "withheld", "investigating", "awaiting_data", "resolved", "waived", "out_of_scope", "scoped", "unscoped"}]
                if any(value != value.lower() for value in statuses):
                    fail(f"{path.relative_to(ROOT)}: machine status enums must be lowercase")
        try:
            validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
            examples = schema.get("examples", [])
            if not isinstance(examples, list) or not examples:
                fail(f"{path.relative_to(ROOT)}: requires at least one fictional valid example")
            for index, example in enumerate(examples, start=1):
                if contains_sensitive_example_value(example):
                    fail(f"{path.relative_to(ROOT)} example {index}: possible secret or private-data field")
                found = list(validator.iter_errors(example))
                if found:
                    fail(f"{path.relative_to(ROOT)} example {index}: {found[0].message}")
        except Exception as exc:
            fail(f"{path.relative_to(ROOT)}: example validation error: {exc}")


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

validate_batch_two_schemas()

if errors:
    print("Knowledge integrity validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Knowledge integrity validation passed.")

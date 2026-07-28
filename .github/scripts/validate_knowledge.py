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
OPENAPI = ROOT / "api" / "openapi"
ACTIONS = ROOT / "config" / "actions"
CONNECTORS = ROOT / "config" / "connectors"
INGESTION = ROOT / "config" / "ingestion"
MAPPINGS = ROOT / "config" / "mappings"
JOBS = ROOT / "config" / "jobs"
EVENTS = ROOT / "api" / "events"
INGESTION_EXAMPLES = ROOT / "examples" / "ingestion"
WIX = ROOT / "config" / "wix"
COMMERCIAL = ROOT / "config" / "commercial"
WIX_EXAMPLES = ROOT / "examples" / "wix"
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


def validate_batch_three_contracts() -> None:
    primary = ("public-resources.openapi.yaml", "api-key-actions.openapi.yaml", "oauth-actions.openapi.yaml", "consolidated-actions.openapi.yaml")
    documents: dict[str, dict] = {}
    operation_ids: set[str] = set()
    for name in ("public-resources.openapi.yaml", "no-auth-actions.openapi.yaml", "api-key-actions.openapi.yaml", "oauth-actions.openapi.yaml", "consolidated-actions.openapi.yaml"):
        path = OPENAPI / name
        document = load_yaml(path)
        if not isinstance(document, dict) or not str(document.get("openapi", "")).startswith("3.1."):
            fail(f"{path.relative_to(ROOT)}: requires OpenAPI 3.1.x")
            continue
        documents[name] = document
        if name not in primary:
            continue
        for item in document.get("paths", {}).values():
            if not isinstance(item, dict):
                continue
            for method, operation in item.items():
                if method.lower() not in {"get", "post", "patch", "put", "delete"} or not isinstance(operation, dict):
                    continue
                operation_id = operation.get("operationId")
                if not operation_id or operation_id in operation_ids:
                    fail(f"{path.relative_to(ROOT)}: missing or duplicate operationId: {operation_id}")
                else:
                    operation_ids.add(operation_id)
                for field in ("summary", "description", "tags", "x-auth-class", "x-execution-mode", "x-risk-class", "x-confirmation-class", "x-idempotency", "x-retry", "x-audit-log", "x-fallback", "responses"):
                    if field not in operation:
                        fail(f"{path.relative_to(ROOT)} {operation_id}: missing {field}")
        for reference in nested_values(document, "$ref"):
            if isinstance(reference, str) and reference.startswith("../schemas/") and not (OPENAPI / reference).resolve().is_file():
                fail(f"{path.relative_to(ROOT)}: unresolved schema reference {reference}")
    routing = load_yaml(ACTIONS / "action-routing.yaml")
    auth = load_yaml(ACTIONS / "action-auth-map.yaml")
    risk = load_yaml(ACTIONS / "action-risk-matrix.yaml")
    budget = load_yaml(ACTIONS / "function-budget.yaml")
    if isinstance(routing, dict):
        routed = set(routing.get("operations", {}))
        if routed != operation_ids:
            fail("config/actions/action-routing.yaml: operation IDs must exactly match primary OpenAPI inventory")
        for name, item in routing.get("operations", {}).items():
            if not isinstance(item, dict) or item.get("function_slot") not in range(1, 11):
                fail(f"config/actions/action-routing.yaml {name}: must map to active function slot 1-10")
    if isinstance(auth, dict):
        mapped = {op for profile in auth.get("auth_classes", {}).values() if isinstance(profile, dict) for op in profile.get("operation_ids", [])}
        if mapped != operation_ids:
            fail("config/actions/action-auth-map.yaml: operation IDs must exactly match primary OpenAPI inventory")
    if isinstance(risk, dict):
        mapped = {op for profile in risk.get("profiles", {}).values() if isinstance(profile, dict) for op in profile.get("operation_ids", [])}
        if not operation_ids.issubset(mapped):
            fail("config/actions/action-risk-matrix.yaml: missing operation risk mapping")
    if not isinstance(budget, dict) or (budget.get("active_function_limit"), budget.get("reserved_function_slots"), budget.get("maximum_total_slots")) != (10, 2, 12):
        fail("config/actions/function-budget.yaml: must preserve 10 active and 2 reserved slots")


def validate_batch_five_contracts() -> None:
    required_connector_ids = {
        "manual_upload", "google_drive", "google_sheets", "shopify", "stripe", "quickbooks", "xero",
        "amazon_seller_central", "walmart_marketplace", "tiktok_shop", "google_ads", "meta_ads",
        "generic_partner_api", "generic_webhook", "cloud_storage", "email_attachment", "internal_agent", "custom_gpt",
    }
    expected_files = [
        *(CONNECTORS / name for name in ("connector-catalog.yaml", "connector-capabilities.yaml", "connector-auth-profiles.yaml", "connector-scope-profiles.yaml", "connector-sync-policies.yaml", "connector-rate-limits.yaml", "connector-account-selection.yaml", "connector-data-retention.yaml", "connector-error-codes.yaml")),
        *(INGESTION / name for name in ("supported-file-types.yaml", "upload-policy.yaml", "file-validation-policy.yaml", "file-routing.yaml", "source-detection.yaml", "data-quality-rules.yaml", "normalization-policy.yaml", "deduplication-policy.yaml", "reconciliation-policy.yaml", "period-alignment-policy.yaml", "redaction-policy.yaml", "quarantine-policy.yaml")),
        *(MAPPINGS / name for name in ("canonical-field-registry.yaml", "canonical-transaction-types.yaml", "canonical-fee-types.yaml", "canonical-source-types.yaml", "provider-field-mappings.yaml", "provider-status-mappings.yaml", "provider-currency-mappings.yaml")),
    ]
    for path in expected_files:
        if not path.exists():
            fail(f"Missing Batch 5 contract: {path.relative_to(ROOT)}")
        else:
            load_yaml(path)

    catalog = load_yaml(CONNECTORS / "connector-catalog.yaml")
    budget = load_yaml(ACTIONS / "function-budget.yaml")
    jobs = load_yaml(JOBS / "job-types.yaml")
    events = load_yaml(EVENTS / "event-catalog.yaml")
    if not isinstance(catalog, dict):
        return
    connector_map = catalog.get("connectors", {})
    if set(connector_map) != required_connector_ids:
        fail("config/connectors/connector-catalog.yaml: connector IDs must exactly match the Batch 5 inventory")
    known_jobs = set(jobs.get("job_types", [])) if isinstance(jobs, dict) else set()
    known_events = set(events.get("event_types", [])) if isinstance(events, dict) else set()
    allowed_routes = {("/api/uploads", 3), ("/api/connectors", 6), ("/api/oauth-callback", 7), ("/api/webhooks/{provider}", 8), ("/api/jobs", 9)}
    for connector_id, connector in connector_map.items():
        if not isinstance(connector, dict):
            fail(f"config/connectors/connector-catalog.yaml {connector_id}: connector must be a mapping")
            continue
        for field in ("provider_id", "current_status", "connection_method", "authentication_profile", "supported_source_types", "supported_file_types", "supported_data_domains", "function_route", "function_slot", "job_types", "emitted_event_types", "fallback_method", "data_sensitivity_classification"):
            if field not in connector:
                fail(f"config/connectors/connector-catalog.yaml {connector_id}: missing {field}")
        if connector.get("current_status") not in {"active", "provisional", "planned", "placeholder", "unsupported"}:
            fail(f"config/connectors/connector-catalog.yaml {connector_id}: invalid current_status")
        route_slot = (connector.get("function_route"), connector.get("function_slot"))
        if route_slot not in allowed_routes:
            fail(f"config/connectors/connector-catalog.yaml {connector_id}: invalid connector route/slot {route_slot}")
        if not set(connector.get("job_types", [])).issubset(known_jobs):
            fail(f"config/connectors/connector-catalog.yaml {connector_id}: references unknown job type")
        if not set(connector.get("emitted_event_types", [])).issubset(known_events):
            fail(f"config/connectors/connector-catalog.yaml {connector_id}: references unknown event type")
    if not isinstance(budget, dict) or (budget.get("active_function_limit"), budget.get("reserved_function_slots"), budget.get("maximum_total_slots")) != (10, 2, 12):
        fail("Batch 5 requires the preserved 10 active and 2 reserved function budget")

    fields = load_yaml(MAPPINGS / "canonical-field-registry.yaml")
    transaction_types = load_yaml(MAPPINGS / "canonical-transaction-types.yaml")
    fee_types = load_yaml(MAPPINGS / "canonical-fee-types.yaml")
    source_types = load_yaml(MAPPINGS / "canonical-source-types.yaml")
    status_mappings = load_yaml(MAPPINGS / "provider-status-mappings.yaml")
    provider_mappings = load_yaml(MAPPINGS / "provider-field-mappings.yaml")
    if isinstance(fields, dict):
        field_names = [item.get("canonical_name") for item in fields.get("fields", []) if isinstance(item, dict)]
        if len(field_names) != 46 or len(field_names) != len(set(field_names)) or None in field_names:
            fail("config/mappings/canonical-field-registry.yaml: expected 46 unique canonical fields")
        for item in fields.get("fields", []):
            if isinstance(item, dict) and not {"data_type", "nullability", "zero_semantics", "unit", "normalization_rule", "example"}.issubset(item):
                fail("config/mappings/canonical-field-registry.yaml: every field requires type, nullability, zero semantics, unit, rule, and example")
    for path, data, key, expected in (
        (MAPPINGS / "canonical-transaction-types.yaml", transaction_types, "transaction_types", 22),
        (MAPPINGS / "canonical-fee-types.yaml", fee_types, "fee_types", 20),
        (MAPPINGS / "canonical-source-types.yaml", source_types, "source_types", 14),
    ):
        values = data.get(key, []) if isinstance(data, dict) else []
        if len(values) != expected or len(values) != len(set(values)):
            fail(f"{path.relative_to(ROOT)}: requires {expected} unique values")
    field_set = {item.get("canonical_name") for item in fields.get("fields", [])} if isinstance(fields, dict) else set()
    if isinstance(provider_mappings, dict):
        for name, profile in provider_mappings.get("profiles", {}).items():
            concepts = profile.get("concepts", {}) if isinstance(profile, dict) else {}
            invalid = set(concepts.values()) - field_set
            if invalid:
                fail(f"config/mappings/provider-field-mappings.yaml {name}: unknown canonical fields {sorted(invalid)}")
    canonical_statuses = set(status_mappings.get("canonical_statuses", [])) if isinstance(status_mappings, dict) else set()
    if canonical_statuses != {"pending", "processing", "completed", "failed", "cancelled", "refunded", "partially_refunded", "disputed", "held", "released", "reversed", "unknown"}:
        fail("config/mappings/provider-status-mappings.yaml: canonical statuses do not match Batch 5 inventory")

    for path in INGESTION_EXAMPLES.glob("*.json"):
        example = load_json(path)
        if example is not None and contains_sensitive_example_value(example):
            fail(f"{path.relative_to(ROOT)}: possible secret or private-data value")
    if len(list(INGESTION_EXAMPLES.glob("*.json"))) != 8:
        fail("examples/ingestion: expected eight fictional JSON examples")


def validate_batch_six_contracts() -> None:
    required_wix = ("wix-site-profile.yaml", "wix-product-mapping.yaml", "wix-pricing-plan-mapping.yaml", "wix-entitlement-mapping.yaml", "wix-member-role-mapping.yaml", "wix-crm-label-mapping.yaml", "wix-form-mapping.yaml", "wix-automation-events.yaml", "wix-webhook-mapping.yaml", "wix-dashboard-linking.yaml", "wix-group-mapping.yaml", "wix-booking-mapping.yaml")
    required_commercial = ("customer-lifecycle.yaml", "subscription-state-machine.yaml", "entitlement-activation-policy.yaml", "upgrade-downgrade-policy.yaml", "cancellation-policy.yaml", "trial-and-founding-member-policy.yaml", "managed-service-intake.yaml", "partner-license-intake.yaml")
    for path in [*(WIX / name for name in required_wix), *(COMMERCIAL / name for name in required_commercial)]:
        if not path.exists():
            fail(f"Missing Batch 6 contract: {path.relative_to(ROOT)}")
        else:
            load_yaml(path)
    site = load_yaml(WIX / "wix-site-profile.yaml")
    products = load_yaml(WIX / "wix-product-mapping.yaml")
    plans = load_yaml(WIX / "wix-pricing-plan-mapping.yaml")
    roles = load_yaml(WIX / "wix-member-role-mapping.yaml")
    labels = load_yaml(WIX / "wix-crm-label-mapping.yaml")
    webhooks = load_yaml(WIX / "wix-webhook-mapping.yaml")
    catalog = load_yaml(PRODUCT_CATALOG)
    product_ids = {item.get("product_id") for item in catalog.get("products", [])} if isinstance(catalog, dict) else set()
    if not isinstance(site, dict) or site.get("site", {}).get("site_id") != "cc61a0cb-edcd-43dc-bdda-42c76443dcd6":
        fail("config/wix/wix-site-profile.yaml: Wix site ID must match the verified property")
    if not isinstance(products, dict) or set(products.get("products", {})) != product_ids:
        fail("config/wix/wix-product-mapping.yaml: product IDs must exactly match Batch 1")
    if not isinstance(plans, dict) or set(plans.get("plans", {})) != {"free_platform_fee_audit_starter", "audit_lab", "margin_control", "guided_margin_recovery", "ecommerce_finance_ops_desk", "partner_agency_license"}:
        fail("config/wix/wix-pricing-plan-mapping.yaml: expected six plan mappings")
    allowed_prices = {"approved", "provisional", "founding_member", "placeholder", "not_applicable"}
    if isinstance(plans, dict):
        for plan in plans.get("plans", {}).values():
            for value in plan.values() if isinstance(plan, dict) else []:
                if isinstance(value, dict) and "status" in value and value["status"] not in allowed_prices:
                    fail("config/wix/wix-pricing-plan-mapping.yaml: invalid price status")
    if not isinstance(roles, dict) or len(roles.get("roles", {})) != len(set(roles.get("roles", {}))):
        fail("config/wix/wix-member-role-mapping.yaml: member roles must be unique")
    if not isinstance(labels, dict) or len(labels.get("labels", {})) != len(set(labels.get("labels", {}).values())):
        fail("config/wix/wix-crm-label-mapping.yaml: CRM labels must be unique")
    if not isinstance(webhooks, dict) or (webhooks.get("defaults", {}).get("route"), webhooks.get("defaults", {}).get("function_slot")) != ("/api/webhooks/{provider}", 8):
        fail("config/wix/wix-webhook-mapping.yaml: Wix webhooks must use slot 8")
    for path in WIX_EXAMPLES.glob("*.json"):
        example = load_json(path)
        if example is not None and contains_sensitive_example_value(example):
            fail(f"{path.relative_to(ROOT)}: possible secret or private-data value")
    if len(list(WIX_EXAMPLES.glob("*.json"))) != 5:
        fail("examples/wix: expected five fictional JSON examples")


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
validate_batch_three_contracts()
validate_batch_five_contracts()
validate_batch_six_contracts()

if errors:
    print("Knowledge integrity validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Knowledge integrity validation passed.")

# OpenAPI Contracts

All contracts use OpenAPI 3.1.0 and placeholder servers. Logical operation paths are contract identifiers; `config/actions/action-routing.yaml` maps every operation to one of the ten shared planned Vercel routes. No OpenAPI path creates a function by itself.

- `public-resources.openapi.yaml` and `no-auth-actions.openapi.yaml` expose public-safe resources only.
- `api-key-actions.openapi.yaml` defines authenticated audit, funding, dispute, upload, export, and automation actions.
- `oauth-actions.openapi.yaml` defines connector authorization and sync actions.
- `consolidated-actions.openapi.yaml` is the top-level inventory and includes internal-only actions.

Schema references resolve to `../schemas/*.schema.json`; credentials, provider secrets, customer data, and real financial information are excluded.

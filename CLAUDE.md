# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Development Commands

```bash
make setup           # Install dependencies (uses uv + .venv)
make dev             # Run local dev server on port 8000
make test            # Run pytest suite
make test-integration  # Run integration tests only (marked with @pytest.mark.integration)
make migrate         # Run Alembic migrations
make audit           # Dependency vulnerability scan
make security-scan   # Bandit static analysis
```

To run a single test: `.venv/bin/python -m pytest tests/test_api.py::test_function_name -v`

## Architecture Overview

This is a FastAPI Books API with Keycloak authentication, Postgres persistence, and OpenTelemetry observability.

### Source Code (`src/`)
- **app.py**: FastAPI application with v1/v2 API routers, middleware stack (security headers, rate limiting, request logging, CORS)
- **auth.py**: JWT verification using PyJWT with JWKS caching; `AuthVerifier` validates tokens against Keycloak; `require_scope()` enforces realm roles
- **service.py**: `BookService` handles CRUD operations using SQLAlchemy ORM
- **entities.py**: SQLAlchemy `BookRecord` model
- **models.py**: Pydantic schemas (`Book`, `CreateBook`, `UpdateBook`)
- **config.py**: `Settings` via pydantic-settings with Vault secret injection support
- **secrets.py**: Vault KV v2 secret fetching
- **otel.py**: OpenTelemetry setup (traces, metrics, logs to OTLP collector)
- **ratelimit.py**: Token bucket rate limiter per IP+token

### Infrastructure (`infra/terraform/`)
- **keycloak/**: Terraform for Keycloak realm, clients, roles, users (this is the source of truth for auth config)
- **vault/**: Terraform for Vault KV secrets

### Observability Stack (docker-compose)
- OTEL Collector → Tempo (traces), Loki (logs), VictoriaMetrics (metrics)
- Grafana with provisioned datasources and dashboards
- Pyroscope for continuous profiling

## Key Configuration

Environment prefix: `APP_` (e.g., `APP_DATABASE_URL`, `APP_KEYCLOAK_ISSUER`)

Important env vars:
- `APP_DATABASE_URL`: Postgres connection string
- `APP_KEYCLOAK_ISSUER`: JWT issuer (must match Keycloak's advertised issuer exactly)
- `APP_VAULT_ADDR` / `APP_VAULT_TOKEN`: Enable Vault secret injection
- `APP_STRICT_SECURITY=true`: Reject default credentials
- `APP_REQUIRE_HTTPS=true`: Enforce HTTPS via x-forwarded-proto

## Testing

Tests are in `tests/` mirroring `src/` structure. Integration tests require Postgres and are marked with `@pytest.mark.integration`.

## Coding Conventions

- Python: 4-space indent, Black-compatible
- camelCase for variables/functions, PascalCase for classes
- Conventional Commits (`feat:`, `fix:`, `chore:`, etc.)

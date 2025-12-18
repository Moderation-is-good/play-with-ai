# play-with-ai

[![CI](https://github.com/moderation-is-good/play-with-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/moderation-is-good/play-with-ai/actions/workflows/ci.yml)
[![Quality and Safety](https://github.com/moderation-is-good/play-with-ai/actions/workflows/quality.yml/badge.svg)](https://github.com/moderation-is-good/play-with-ai/actions/workflows/quality.yml)
[![CodeQL](https://github.com/moderation-is-good/play-with-ai/actions/workflows/codeql.yml/badge.svg)](https://github.com/moderation-is-good/play-with-ai/actions/workflows/codeql.yml)

FastAPI + Keycloak–secured books API with Postgres, Vault, and a full observability stack (OTel/Tempo/Loki/VictoriaMetrics/Grafana/Pyroscope). Built with uv, instrumented for traces/logs/metrics, and hardened CI/CD (lint, tests, security scans, SBOM).

## Running locally
- Install deps: `uv pip install --system -r requirements.txt`
- Start stack: `docker compose up -d`
- Run app: `uvicorn src.app:app --reload`

## CI/CD summary
- **CI**: unit tests with coverage on a Postgres service, SBOM via Syft, multi-arch image build to GHCR.
- **Quality and Safety**: ruff/bandit/mypy, pip-audit, coverage upload, integration smoke (Keycloak/Tempo/Loki).
- **Security**: gitleaks secret scan, CodeQL static analysis.

See `AGENTS.md` for deeper operational notes.

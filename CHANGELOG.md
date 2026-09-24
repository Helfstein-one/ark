# Changelog

All notable changes to Project A.R.K. (Autonomous AI Resource Kernel) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Comprehensive architecture diagrams (Mermaid) in `README.md` and `docs/architecture.md`.
- End-to-end user & developer journey ("Jornada de Uso") documentation and sequence diagrams.
- Extended documentation covering the monitoring & observability stack (Prometheus, Grafana, cAdvisor).
- Project changelog tracking initial releases and epic completions.

---

## [1.0.0] - 2026-09-24

### Added
- **Document Ingestion Skill (`Epic 9`)**:
  - Implemented `skills/document_ingester.py` supporting PDF (`PyPDF2`) and raw text document parsing into configurable semantic chunks.
  - Exposed `ingest_document` tool endpoint on FastAPI Skills Layer (`skills/main.py`).
  - Added unit and integration tests for document ingestion in `tests/test_integration.py`.
- **Monitoring & Observability Stack (`Epic 7`)**:
  - Integrated `cAdvisor` (container metrics exporter), `Prometheus` (time-series database), and `Grafana` (visualization).
  - Automated JSON dashboard provisioning (`container_metrics.json`).
  - Added persistent named volumes `prometheus_data` and `grafana_data`.
- **Modular Python Skills Layer (`Epic 4`)**:
  - FastAPI framework implementation for tool discovery (`GET /tools`) and tool invocation (`POST /tools/call`).
  - Containerized skills service (`skills/Dockerfile`) integrated into `docker-compose.yml` on port `8001`.
  - Implemented `code_quality_analyzer.py` for automated code inspection.
- **Nginx Reverse Proxy & Network Security (`Epic 1 & 3`)**:
  - Secure TLS termination via Nginx routing HTTPS (`:443`/`:8443`) to Open WebUI (`:8080`).
  - Strict network isolation on `ark_network`: Ollama (`:11434`) direct host port exposure removed.
- **Cross-Platform Bootstrapping & Automation**:
  - Added `scripts/bootstrap.sh` (Linux/Mac) and `scripts/bootstrap.ps1` (Windows).
  - Automated local self-signed SSL/TLS certificate generation (`scripts/generate-certs.sh`).
  - Added automated model pulling script (`scripts/pull-models.sh`).
  - Added Makefile with helper targets (`up`, `down`, `logs`, `clean`, `pull-models`).

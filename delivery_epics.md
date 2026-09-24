# Project A.R.K - Delivery Epics & Tasks

## Epic 1: Container Orchestration & Infrastructure Completion
**Description**: Finalize the local containerized ecosystem to ensure all services can communicate and be managed reliably.
* **Task 1.1**: Review and finalize `docker-compose.yml` for network and volume persistence.
* **Task 1.2**: Enhance `Makefile` with commands for logging, testing, and clean teardowns.
* **Task 1.3**: Complete bootstrap scripts for cross-platform support (Mac/Linux/Windows).

## Epic 2: Model Management & Inference Layer (Ollama)
**Description**: Operationalize the Ollama service for seamless local model inference.
* **Task 2.1**: Automate downloading of default LLMs (e.g., Llama 3) on initial boot.
* **Task 2.2**: Configure resource constraints (CPU/GPU) in Docker for Ollama.
* **Task 2.3**: Establish health checks and auto-restart policies for the Ollama container.

## Epic 3: UI & RAG Integration (Open WebUI)
**Description**: Set up Open WebUI as the unified interface and enable Retrieval-Augmented Generation capabilities.
* **Task 3.1**: Connect Open WebUI to the local Ollama instance securely.
* **Task 3.2**: Configure vector database storage and embedding models within the ecosystem for RAG.
* **Task 3.3**: Customize the Open WebUI interface (branding, default system prompts) for the project.

## Epic 4: Modular Python Skills Layer
**Description**: Develop and integrate the extensible Python layer for custom skills and tool calling.
* **Task 4.1**: Define standard API structure for Python skill modules (e.g., using FastAPI).
* **Task 4.2**: Implement core tools (e.g., web search, file system operations, API connectors).
* **Task 4.3**: Integrate the Python skills layer with Open WebUI's external tool/function calling interface.
* **Task 4.4**: Containerize the Python skills layer and add it to the `docker-compose.yml`.

## Epic 5: Testing, CI/CD, and Deployment
**Description**: Ensure stability and ease of deployment for Project A.R.K.
* **Task 5.1**: Write integration tests ensuring Ollama, Open WebUI, and Skills Layer communicate properly.
* **Task 5.2**: Create GitHub Actions (or equivalent CI) for linting and testing the Python code.
* **Task 5.3**: Finalize user-facing documentation (`README.md`) with Quickstart, Architecture, and Troubleshooting sections.

## Epic 7: Monitoring & Observability Stack
**Description**: Implement monitoring for the local infrastructure to track CPU/Memory usage and WebUI traffic.
* **Task 7.1**: Add Prometheus and Grafana services to `docker-compose.yml`.
* **Task 7.2**: Configure a basic Grafana dashboard (via JSON provisioning) to track Docker/Podman container metrics (e.g., using cAdvisor).
* **Task 7.3**: Ensure monitoring volumes are persisted securely.

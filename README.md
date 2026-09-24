# Project A.R.K.

Project A.R.K. is a complete, containerized ecosystem integrating Ollama, Open WebUI, and a Modular Python Skills Layer for rapid development of localized LLM capabilities.

## Architecture

* **Ollama**: Local inference server exposing models at `11434`.
* **Open WebUI**: The web interface (port `8000`) for seamless user interaction and RAG integration, connected securely to Ollama.
* **Skills Layer**: A FastAPI-based modular skill and tool execution layer (port `8001`), providing tools to be leveraged by the Open WebUI.
* **Monitoring & Observability**:
  * **cAdvisor**: Collects container resource usage and performance metrics (port `8082`).
  * **Prometheus**: Scrapes and stores metrics (port `9090`).
  * **Grafana**: Visualization dashboard for container metrics (port `3000`).

## Quickstart

### Prerequisites
* Docker and Docker Compose (or Podman and podman-compose for rootless execution).

### Installation (Linux / Mac)
Run the bootstrap script to start everything automatically:
```bash
./scripts/bootstrap.sh
```

### Installation (Windows)
Run the provided PowerShell bootstrap script:
```powershell
.\scripts\bootstrap.ps1
```

### Manual Usage
You can also use the Makefile:
* `make up`: Start all containers in the background.
* `make down`: Stop all containers.
* `make logs`: View combined logs.
* `make pull-models`: Pull default models for Ollama.
* `make clean`: Completely teardown containers and volumes.

## Troubleshooting

* **Permission Errors with Volumes:**
  If you are running in a strict Podman rootless environment, you might face permission issues with volumes. The `docker-compose.yml` mounts local directories with `:z` for SELinux relabeling. Ensure your local `./scripts` folder has execution permissions.

* **Ollama Health Check Fails:**
  The healthcheck expects the container to respond to `ollama list`. If it continues to fail, check the logs via `make logs`. It might be pulling a very large model for the first time.

* **Open WebUI doesn't connect to Ollama:**
  Ensure the `ark_network` bridge is working correctly and `OLLAMA_BASE_URL` is set to `http://ollama:11434` in `docker-compose.yml`.

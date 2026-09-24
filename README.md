# Project A.R.K.

Project A.R.K. is a complete, containerized ecosystem integrating Ollama, Open WebUI, a Reverse Proxy (Nginx), and a Modular Python Skills Layer for rapid development of localized LLM capabilities.

## Architecture

* **Reverse Proxy (Nginx)**: Secure entry point routing HTTPS traffic (ports `443` / `8443`) to Open WebUI and enforcing internal network isolation.
* **Open WebUI**: The web interface proxied securely via HTTPS for seamless user interaction and RAG integration, connected securely to Ollama.
* **Ollama**: Local inference server on the internal container network (`11434`), strictly restricted from public host access.
* **Skills Layer**: A FastAPI-based modular skill and tool execution layer (port `8001`), providing tools to be leveraged by the Open WebUI.

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
Before running manually, ensure self-signed SSL/TLS certificates are generated:
```bash
./scripts/generate-certs.sh
```

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

* **SSL Certificate Warnings:**
  Self-signed certificates are generated for local development. Accept the certificate warning in your browser when accessing `https://localhost`.

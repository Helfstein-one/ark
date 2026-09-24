Write-Host "Generating SSL certificates..."
& "$PSScriptRoot\generate-certs.sh"

Write-Host "Starting Project A.R.K. containers..."
docker compose up -d

Write-Host "Waiting for containers to initialize (15 seconds)..."
Start-Sleep -Seconds 15

Write-Host "Pulling default LLMs..."
docker compose exec ollama /scripts/pull-models.sh

Write-Host "Bootstrap complete. Services are ready."

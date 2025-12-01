Param(
  [string]$ProjectId = $(gcloud config get-value project 2>$null),
  [string]$Region = 'us-central1'
)

if (-not $ProjectId) {
  Write-Error "Project ID not provided and not set in gcloud. Run 'gcloud config set project <PROJECT_ID>' or pass it as -ProjectId."; exit 1
}

$serviceName = 'travel-agent-demo'
$image = "gcr.io/$ProjectId/$serviceName"

Write-Host "Building container and submitting to Cloud Build..."
gcloud builds submit --tag $image

Write-Host "Deploying to Cloud Run ($Region)..."
# Ensure secret OPENAI_API_KEY exists in Secret Manager before running this.
gcloud run deploy $serviceName --image $image --region $Region --platform managed --allow-unauthenticated --set-secrets OPENAI_API_KEY=OPENAI_API_KEY:latest

Write-Host "Deployed $serviceName to Cloud Run (region=$Region)."

Write-Host "If you need to create the secret, run (PowerShell):"
Write-Host "  'sk-...' | gcloud secrets create OPENAI_API_KEY --data-file=- --replication-policy=automatic"
Write-Host "And grant Cloud Build permission to access the secret (example):"
Write-Host "  gcloud secrets add-iam-policy-binding OPENAI_API_KEY --member='serviceAccount:$(gcloud projects describe $ProjectId --format='value(projectNumber)')@cloudbuild.gserviceaccount.com' --role='roles/secretmanager.secretAccessor'"

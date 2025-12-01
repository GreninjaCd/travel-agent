#!/bin/bash
set -euo pipefail

# Example deploy script for Google Cloud Run (adjust service name and region)
# Usage:
#   ./infra/cloudrun-deploy.sh <PROJECT_ID> [REGION]

PROJECT_ID=${1:-$(gcloud config get-value project 2>/dev/null)}
REGION=${2:-us-central1}
SERVICE_NAME="travel-agent-demo"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

if [[ -z "$PROJECT_ID" ]]; then
	echo "Project ID not provided and not set in gcloud. Run 'gcloud config set project <PROJECT_ID>' or pass it as the first arg." >&2
	exit 1
fi

echo "Building container and pushing to ${IMAGE}..."
gcloud builds submit --tag ${IMAGE}

echo "Deploying to Cloud Run (${REGION})..."
# Ensure the secret OPENAI_API_KEY exists in Secret Manager before running this deploy.
gcloud run deploy ${SERVICE_NAME} \
	--image ${IMAGE} \
	--region ${REGION} \
	--platform managed \
	--allow-unauthenticated \
	--set-secrets OPENAI_API_KEY=OPENAI_API_KEY:latest

echo "Deployed ${SERVICE_NAME} to Cloud Run (region=${REGION})."

echo "If you need to create the secret, run:"
echo "  echo 'sk-...' | gcloud secrets create OPENAI_API_KEY --data-file=- --replication-policy=automatic"
echo "Then allow Cloud Run (or Cloud Build) service account access to the secret:"
echo "  gcloud secrets add-iam-policy-binding OPENAI_API_KEY --member='serviceAccount:$(gcloud projects describe ${PROJECT_ID} --format='value(projectNumber)')@cloudbuild.gserviceaccount.com' --role='roles/secretmanager.secretAccessor'"

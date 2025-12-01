# Travel Agent

Multi-tier travel assistant: Node.js (Express) front-end + Python (FastAPI agents) backend.

**Structure:**
- `src/` - Express server + Python agent client
- `app/` - Python agents, tools, memory
- `infra/` - deployment scripts
- `demo/` - sample requests

**Quick start (local dev)**

```powershell
# Python venv
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Node deps
npm install

# Run (Node server calls Python CLI)
npm start
```

Server will listen on `http://localhost:3000`.

**Test the agent**

```powershell
curl -X POST http://localhost:3000/api/travel `
  -H "Content-Type: application/json" `
  -d '@demo/sample_request.json'
```

OpenAI notes
 - To enable OpenAI-based summaries set `OPENAI_API_KEY` in your environment or in Cloud Run.
 - Locally, copy `.env.example` to `.env` and set the key, or export the variable before running.

Cloud Run: pass the key to your service via `--set-env-vars OPENAI_API_KEY=YOUR_KEY` when running `gcloud run deploy`.

**Deploying to Cloud Run (recommended flow with Secret Manager)**

1. Choose a Google Cloud project and enable APIs:

```powershell
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable cloudbuild.googleapis.com run.googleapis.com secretmanager.googleapis.com
```

2. Create a Secret Manager secret containing your OpenAI (or other) key:

```powershell
# Windows PowerShell
"sk-..." | gcloud secrets create OPENAI_API_KEY --data-file=- --replication-policy=automatic

# or on Linux/macOS
# echo "sk-..." | gcloud secrets create OPENAI_API_KEY --data-file=- --replication-policy=automatic
```

3. Grant the Cloud Build service account access to read the secret (replace PROJECT_ID):

```powershell
gcloud secrets add-iam-policy-binding OPENAI_API_KEY \
  --member="serviceAccount:$(gcloud projects describe YOUR_PROJECT_ID --format='value(projectNumber)')@cloudbuild.gserviceaccount.com" \
  --role='roles/secretmanager.secretAccessor'
```

4. Build and deploy using the included helper script (bash or PowerShell):

```powershell
# Bash
./infra/cloudrun-deploy.sh YOUR_PROJECT_ID us-central1

# PowerShell
.\infra\deploy.ps1 -ProjectId YOUR_PROJECT_ID -Region us-central1
```

The helper script will submit a Cloud Build that builds the container and then deploys to Cloud Run, binding the `OPENAI_API_KEY` secret into the runtime.

Notes:
- The Cloud Build service account must have permission to access the secret (see step 3).
- In production prefer to use Secret Manager and fine-grained service accounts rather than passing raw keys as `--set-env-vars`.
- If you want automatic CI/CD, create a Cloud Build trigger that runs on commits to `main` and uses `infra/cloudbuild.yaml`.

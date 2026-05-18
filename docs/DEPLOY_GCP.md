# 🚀 Google Cloud Run (Serverless Containers) Deployment Guide

This guide details the complete serverless architecture of the **Sentience Layer Cognitive Backend** and provides step-by-step instructions on deploying the Python FastAPI engine to **Google Cloud Run** and linking it with a **Google Cloud SQL PostgreSQL** relational database instance.

---

## 🏛️ GCP Architecture Blueprint

Deploying to Google Cloud Run leverages enterprise-grade, serverless scalability, perfect for a Google-centric hackathon showcase:

1. **Google Artifact Registry**: Hosts the Docker container compiled from your local Python codebase.
2. **Google Cloud Builds**: Compiles the Docker image directly in the cloud (no local Docker daemon required!).
3. **Google Cloud SQL (PostgreSQL)**: Serves as the stateful relational memory repository for agents and traces.
4. **Google Cloud Run**: Runs the FastAPI app serverless, automatically scaling container count based on active load (scaling down to `0` when idle to conserve billing credits).

---

## 🛠️ Automated Deployment Script

We have created two fully automated deployment scripts in your repository root:
- [deploy-gcp.ps1](file:///c:/Users/catac/OneDrive/Desktop/sentience-layer/deploy-gcp.ps1) — **Windows PowerShell Script** (Recommended)
- [deploy-gcp.sh](file:///c:/Users/catac/OneDrive/Desktop/sentience-layer/deploy-gcp.sh) — **Bash Script for macOS/Linux**

These scripts sequentially handle authentication, API activation, container compilation, database provisioning, credential mapping, and service linking in one run.

---

## 📋 Step-by-Step Deployment Steps

### Step 1: Install the Google Cloud SDK (gcloud CLI)
To deploy, you must have the `gcloud` CLI installed on your local computer.

- **Windows**: Download and run the [Google Cloud CLI Installer](https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe) and follow the onscreen setup instructions.
- **macOS / Linux**: Open a terminal and run:
  ```bash
  curl https://sdk.cloud.google.com | bash
  exec -l $SHELL
  ```

*Verification:* Restart your terminal and verify the CLI is operational:
```bash
gcloud --version
```

---

### Step 2: Create a GCP Project & Enable Billing
1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project selector dropdown in the top-left and select **New Project**.
3. Name your project (e.g., `sentenceproject-496712`) and copy the **Project ID** (e.g., `sentenceproject-496712`).
4. Ensure a **Billing Account** is active and linked to this project (required to enable Cloud SQL and Cloud Build engines).

---

### Step 3: Run the Automated Deployment Script
Open your PowerShell (on Windows) or Bash terminal in the root `sentience-layer` directory.

#### Windows PowerShell:
```powershell
# Set ExecutionPolicy to allow local script runs
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Run the deployment script with your Project ID
.\deploy-gcp.ps1 -ProjectID "sentenceproject-496712"
```

#### macOS / Linux:
```bash
# Set executable permissions
chmod +x deploy-gcp.sh

# Run the script with your Project ID
./deploy-gcp.sh --project "sentenceproject-496712"
```

#### What the script does under the hood:
1. Opens your browser to authenticate with your Google account (`gcloud auth login`).
2. Configures `gcloud` to target your specified Project ID.
3. Automatically enables `run`, `sqladmin`, `artifactregistry`, and `cloudbuild` APIs.
4. Creates a Docker registry repository in your selected region.
5. Builds and pushes your Python FastAPI container using Cloud Builds.
6. Provisions a highly cost-efficient `db-f1-micro` tier PostgreSQL 14 instance on Cloud SQL.
7. Generates database user credentials and maps environment connections securely.
8. Deploys the container to Cloud Run with scale-to-zero capabilities enabled.

---

### Step 4: Link Your Deployed Backend to the Frontend
Once the script completes, it will print your **Live Backend API URL** (e.g. `https://sentience-backend-a7b8e-uc.a.run.app`).

To route your statically hosted Firebase frontend to this live cloud server:

1. Navigate to the `frontend/` directory and create or edit `.env.production`:
   ```env
   NEXT_PUBLIC_API_URL=https://sentience-backend-a7b8e-uc.a.run.app
   NEXT_PUBLIC_WS_URL=wss://sentience-backend-a7b8e-uc.a.run.app/ws
   ```
2. Redeploy the frontend:
   ```bash
   npm run firebase:deploy
   ```

Your Firebase CDN frontend is now connected to your secure, scalable Google Cloud Run cognitive backend serverless gateway! 🎉

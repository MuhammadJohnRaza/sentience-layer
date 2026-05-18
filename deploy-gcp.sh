#!/usr/bin/env bash
# 🚀 Google Cloud Run & Cloud SQL Automated Deployment Script (Bash for Linux/macOS)
# Sentience Layer Cognitive Backend Deployment

set -e

# Default parameters
PROJECT_ID=""
REGION="us-central1"
SQL_INSTANCE="sentience-db-instance"
SQL_PASSWORD="SentienceSecurePass123!"

echo -e "\033[0;36m==============================================================\033[0m"
echo -e "\033[0;36m🧠 Sentience Layer - Google Cloud Run Deployment Engine (Bash)\033[0m"
echo -e "\033[0;36m==============================================================\033[0m"

# Step 1: Verify gcloud installation
if ! command -v gcloud &> /dev/null; then
    echo -e "\033[0;31m❌ Error: Google Cloud SDK (gcloud CLI) is not installed on this system.\033[0m"
    echo -e "\033[0;33mPlease download and install it from:\033[0m"
    echo -e "\033[0;34m👉 https://cloud.google.com/sdk/docs/install\033[0m"
    echo -e "\033[0;33mAfter installation, restart your terminal and rerun this script.\033[0m"
    exit 1
fi

# Parse parameters
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -p|--project) PROJECT_ID="$2"; shift ;;
        -r|--region) REGION="$2"; shift ;;
        -i|--instance) SQL_INSTANCE="$2"; shift ;;
        -s|--password) SQL_PASSWORD="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Step 2: Validate Project ID
if [ -z "$PROJECT_ID" ]; then
    echo -e "\033[0;33m⚠️ Warning: No GCP Project ID specified. Fetching active config project...\033[0m"
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null || true)
    if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" == "(unset)" ]; then
        echo -e "\033[0;31m❌ Error: No active GCP project found. Please pass the project ID:\033[0m"
        echo -e "\033[0;33mExample: ./deploy-gcp.sh --project 'my-gcp-project-123'\033[0m"
        exit 1
    fi
fi

echo -e "\033[0;32m🌐 Using GCP Project ID: $PROJECT_ID\033[0m"
echo -e "\033[0;32m📍 Deployment Region: $REGION\033[0m"
echo -e "\033[0;32m💾 Cloud SQL Instance: $SQL_INSTANCE\033[0m"

# Step 3: Authenticate gcloud
echo -e "\n\033[0;36m🔑 Step 1: Authenticating with Google Cloud...\033[0m"
active_account=$(gcloud auth list --filter="status=ACTIVE" --format="value(account)" 2>/dev/null || true)
if [ -z "$active_account" ]; then
    gcloud auth login
else
    echo -e "\033[0;32m✅ Already authenticated as: $active_account\033[0m"
fi

# Step 4: Configure Project
echo -e "\n\033[0;36m⚙️ Step 2: Setting active project configuration...\033[0m"
gcloud config set project "$PROJECT_ID"

# Step 5: Enable APIs
echo -e "\n\033[0;36m🔌 Step 3: Enabling Google Cloud APIs (this may take a minute)...\033[0m"
gcloud services enable \
    run.googleapis.com \
    sqladmin.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com

# Step 6: Create Artifact Registry
echo -e "\n\033[0;36m📦 Step 4: Creating Google Artifact Registry Repository...\033[0m"
if ! gcloud artifacts repositories describe sentience-repo --location="$REGION" &>/dev/null; then
    gcloud artifacts repositories create sentience-repo \
        --repository-format=docker \
        --location="$REGION" \
        --description="Sentience Layer Container Images"
else
    echo -e "\033[0;32m✅ Artifact Registry 'sentience-repo' already exists.\033[0m"
fi

# Step 7: Build Container via Google Cloud Build
echo -e "\n\033[0;36m🛠️ Step 5: Submitting build to Google Cloud Builds...\033[0m"
IMAGE_TAG="$REGION-docker.pkg.dev/$PROJECT_ID/sentience-repo/backend-python:latest"

# Copy sentience_kernel module into python backend workspace for Docker packaging
echo "Copying sentience_kernel into backend/python/ for container build..."
rm -rf ./backend/python/sentience_kernel
cp -r ./sentience_kernel ./backend/python/

gcloud builds submit --tag "$IMAGE_TAG" ./backend/python

# Step 8: Provision PostgreSQL on Cloud SQL
echo -e "\n\033[0;36m💾 Step 6: Checking/Creating Google Cloud SQL PostgreSQL database...\033[0m"
if ! gcloud sql instances describe "$SQL_INSTANCE" &>/dev/null; then
    echo -e "\033[0;33m🆕 Provisioning new PostgreSQL 14 instance ($SQL_INSTANCE). This will take 5-10 minutes...\033[0m"
    gcloud sql instances create "$SQL_INSTANCE" \
        --database-version=POSTGRES_14 \
        --tier=db-f1-micro \
        --region="$REGION" \
        --root-password="$SQL_PASSWORD"
else
    echo -e "\033[0;32m✅ Cloud SQL instance '$SQL_INSTANCE' already exists.\033[0m"
fi

# Step 9: Create Databases and User Profiles
echo -e "\n\033[0;36m👤 Step 7: Configuring database schemas and credentials...\033[0m"
db_check=$(gcloud sql databases list --instance="$SQL_INSTANCE" --filter="name=sentience_db" --format="value(name)" || true)
if [ -z "$db_check" ]; then
    gcloud sql databases create sentience_db --instance="$SQL_INSTANCE"
fi

user_check=$(gcloud sql users list --instance="$SQL_INSTANCE" --filter="name=sentience" --format="value(name)" || true)
if [ -z "$user_check" ]; then
    gcloud sql users create sentience --instance="$SQL_INSTANCE" --password="$SQL_PASSWORD"
fi

# Step 10: Deploy to Google Cloud Run
echo -e "\n\033[0;36m🚀 Step 8: Deploying Cognitive Backend to Google Cloud Run...\033[0m"
CONNECTION_NAME="$PROJECT_ID:$REGION:$SQL_INSTANCE"
DB_URL="postgresql://sentience:$SQL_PASSWORD@/sentience_db?host=/cloudsql/$CONNECTION_NAME"

gcloud run deploy sentience-backend \
    --image "$IMAGE_TAG" \
    --region "$REGION" \
    --port 8000 \
    --add-cloudsql-instances "$CONNECTION_NAME" \
    --set-env-vars "DATABASE_URL=$DB_URL,APP_ENV=production,APP_DEBUG=false" \
    --allow-unauthenticated

# Step 11: Display Output URL
SERVICE_URL=$(gcloud run services describe sentience-backend --region="$REGION" --format="value(status.url)")
echo -e "\n\033[0;32m==============================================================\033[0m"
echo -e "\033[0;32m🎉 CONGRATULATIONS! DEPLOYMENT SUCCESSFULLY COMPLETED!\033[0m"
echo -e "\033[0;32m==============================================================\033[0m"
echo -e "\033[0;32m🌍 Live Backend API URL: $SERVICE_URL\033[0m"
echo -e "\033[0;32m⚡ Live WebSocket Telemetry: ws://${SERVICE_URL#https://}/ws\033[0m"
echo -e "\033[0;32m==============================================================\033[0m"
echo -e "\033[0;33m👉 Update NEXT_PUBLIC_API_URL and NEXT_PUBLIC_WS_URL in your frontend .env and redeploy to Firebase!\033[0m"

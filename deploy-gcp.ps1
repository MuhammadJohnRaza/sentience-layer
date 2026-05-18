# 🚀 Google Cloud Run & Cloud SQL Automated Deployment Script (Windows PowerShell)
# Sentience Layer Cognitive Backend Deployment

param (
    [string]$ProjectID = "",
    [string]$Region = "us-central1",
    [string]$SqlInstance = "sentience-db-instance",
    [string]$SqlPassword = "SentienceSecurePass123!"
)

Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "🧠 Sentience Layer - Google Cloud Run Deployment Engine" -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan

# Step 1: Verify gcloud installation
$gcloudCheck = Get-Command gcloud -ErrorAction SilentlyContinue
if ($null -eq $gcloudCheck) {
    Write-Host "❌ Error: Google Cloud SDK (gcloud CLI) is not installed on this system." -ForegroundColor Red
    Write-Host "Please download and install it from:" -ForegroundColor Yellow
    Write-Host "👉 https://cloud.google.com/sdk/docs/install#windows" -ForegroundColor Yellow
    Write-Host "After installation, restart your terminal and rerun this script." -ForegroundColor Yellow
    Exit 1
}

# Step 2: Validate Project ID
if ([string]::IsNullOrEmpty($ProjectID)) {
    Write-Host "⚠️ Warning: No GCP Project ID specified. Fetching your active gcloud project..." -ForegroundColor Yellow
    $ProjectID = (gcloud config get-value project 2>$null)
    if ([string]::IsNullOrEmpty($ProjectID) -or $ProjectID -eq "(unset)") {
        Write-Host "❌ Error: No active GCP project found. Please pass the ProjectID parameter:" -ForegroundColor Red
        Write-Host "Example: .\deploy-gcp.ps1 -ProjectID 'my-gcp-project-123'" -ForegroundColor Yellow
        Exit 1
    }
}

Write-Host "🌐 Using GCP Project ID: $ProjectID" -ForegroundColor Green
Write-Host "📍 Deployment Region: $Region" -ForegroundColor Green
Write-Host "💾 Cloud SQL Instance: $SqlInstance" -ForegroundColor Green

# Step 3: Authenticate gcloud
Write-Host "`n🔑 Step 1: Authenticating with Google Cloud..." -ForegroundColor Cyan
gcloud auth login

# Step 4: Configure Project
Write-Host "`n⚙️ Step 2: Setting active project configuration..." -ForegroundColor Cyan
gcloud config set project $ProjectID

# Step 5: Enable APIs
Write-Host "`n🔌 Step 3: Enabling Google Cloud APIs (this may take a minute)..." -ForegroundColor Cyan
gcloud services enable `
    run.googleapis.com `
    sqladmin.googleapis.com `
    artifactregistry.googleapis.com `
    cloudbuild.googleapis.com

# Step 6: Create Artifact Registry
Write-Host "`n📦 Step 4: Creating Google Artifact Registry Repository..." -ForegroundColor Cyan
$repoCheck = gcloud artifacts repositories describe sentience-repo --location=$Region 2>$null
if ($null -eq $repoCheck) {
    gcloud artifacts repositories create sentience-repo `
        --repository-format=docker `
        --location=$Region `
        --description="Sentience Layer Container Images"
} else {
    Write-Host "✅ Artifact Registry 'sentience-repo' already exists." -ForegroundColor Green
}

# Step 7: Build Container via Google Cloud Build (No local Docker needed!)
Write-Host "`n🛠️ Step 5: Submitting build to Google Cloud Builds..." -ForegroundColor Cyan
$ImageTag = "$Region-docker.pkg.dev/$ProjectID/sentience-repo/backend-python:latest"
gcloud builds submit --tag $ImageTag ./backend/python

# Step 8: Provision PostgreSQL on Cloud SQL
Write-Host "`n💾 Step 6: Checking/Creating Google Cloud SQL PostgreSQL database..." -ForegroundColor Cyan
$sqlCheck = gcloud sql instances describe $SqlInstance 2>$null
if ($null -eq $sqlCheck) {
    Write-Host "🆕 Provisioning new PostgreSQL 14 instance ($SqlInstance). This will take 5-10 minutes..." -ForegroundColor Yellow
    gcloud sql instances create $SqlInstance `
        --database-version=POSTGRES_14 `
        --tier=db-f1-micro `
        --region=$Region `
        --root-password=$SqlPassword
} else {
    Write-Host "✅ Cloud SQL instance '$SqlInstance' already exists." -ForegroundColor Green
}

# Step 9: Create Databases and User Profiles
Write-Host "`n👤 Step 7: Configuring database schemas and credentials..." -ForegroundColor Cyan
# Create database
$dbCheck = gcloud sql databases list --instance=$SqlInstance --filter="name=sentience_db" --format="value(name)"
if ([string]::IsNullOrEmpty($dbCheck)) {
    gcloud sql databases create sentience_db --instance=$SqlInstance
}
# Create user
$userCheck = gcloud sql users list --instance=$SqlInstance --filter="name=sentience" --format="value(name)"
if ([string]::IsNullOrEmpty($userCheck)) {
    gcloud sql users create sentience --instance=$SqlInstance --password=$SqlPassword
}

# Step 10: Deploy to Google Cloud Run
Write-Host "`n🚀 Step 8: Deploying Cognitive Backend to Google Cloud Run..." -ForegroundColor Cyan
$ConnectionName = "$ProjectID:$Region:$SqlInstance"
$DbUrl = "postgresql://sentience:$SqlPassword@/sentience_db?host=/cloudsql/$ConnectionName"

gcloud run deploy sentience-backend `
    --image $ImageTag `
    --region $Region `
    --add-cloudsql-instances $ConnectionName `
    --set-env-vars "DATABASE_URL=$DbUrl,APP_ENV=production,APP_DEBUG=false" `
    --allow-unauthenticated

# Step 11: Display Output URL
$ServiceUrl = gcloud run services describe sentience-backend --region=$Region --format="value(status.url)"
Write-Host "`n==============================================================" -ForegroundColor Green
Write-Host "🎉 CONGRATULATIONS! DEPLOYMENT SUCCESSFULLY COMPLETED!" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green
Write-Host "🌍 Live Backend API URL: $ServiceUrl" -ForegroundColor Green
Write-Host "⚡ Live WebSocket Telemetry: ws://$($ServiceUrl.Replace('https://', ''))/ws" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green
Write-Host "👉 Update NEXT_PUBLIC_API_URL and NEXT_PUBLIC_WS_URL in your frontend .env and redeploy to Firebase!" -ForegroundColor Yellow

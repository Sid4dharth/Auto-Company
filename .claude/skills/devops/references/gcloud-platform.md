# Google Cloud Platform with gcloud CLI

Comprehensive guide for gcloud CLI - command-line interface for Google Cloud Platform.

## Installation

### Linux
```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xf google-cloud-cli-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh
./google-cloud-sdk/bin/gcloud init
```

### Debian/Ubuntu
```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get update && sudo apt-get install google-cloud-cli
```

### macOS
```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-arm.tar.gz
tar -xf google-cloud-cli-darwin-arm.tar.gz
./google-cloud-sdk/install.sh
```

## Authentication

### User Account
```bash
# Login with browser
gcloud auth login

# Login without browser (remote/headless)
gcloud auth login --no-browser

# List accounts
gcloud auth list

# Switch account
gcloud config set account user@example.com
```

### Service Account
```bash
# Activate with key file
gcloud auth activate-service-account SA_EMAIL --key-file=key.json

# Create service account
gcloud iam service-accounts create SA_NAME \
  --display-name="Service Account"

# Create key
gcloud iam service-accounts keys create key.json \
  --iam-account=SA_EMAIL

# Grant role
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/compute.admin"
```

### Service Account Impersonation (Recommended)
```bash
# Impersonate for single command
gcloud compute instances list \
  --impersonate-service-account=SA_EMAIL

# Set default impersonation
gcloud config set auth/impersonate_service_account SA_EMAIL

# Clear impersonation
gcloud config unset auth/impersonate_service_account
```

Why impersonation? Short-lived credentials, no key files, centralized management.

## Configuration Management

### Named Configurations
```bash
# Create configuration
gcloud config configurations create dev

# List configurations
gcloud config configurations list

# Activate configuration
gcloud config configurations activate dev

# Set properties
gcloud config set project my-project-dev
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# View properties
gcloud config list

# Delete configuration
gcloud config configurations delete dev
```

### Multi-Environment Pattern
```bash
# Development
gcloud config configurations create dev
gcloud config set project my-project-dev
gcloud config set account dev@example.com

# Staging
gcloud config configurations create staging
gcloud config set project my-project-staging
gcloud config set auth/impersonate_service_account staging-sa@project.iam.gserviceaccount.com

# Production
gcloud config configurations create prod
gcloud config set project my-project-prod
gcloud config set auth/impersonate_service_account prod-sa@project.iam.gserviceaccount.com
```

## Project Management

```bash
# List projects
gcloud projects list

# Create project
gcloud projects create PROJECT_ID --name="Project Name"

# Set active project
gcloud config set project PROJECT_ID

# Get current project
gcloud config get-value project

# Enable API
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com

# List enabled APIs
gcloud services list
```

## Output Formats

```bash
# JSON (recommended for scripting)
gcloud compute instances list --format=json

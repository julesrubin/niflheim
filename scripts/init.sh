#!/bin/bash

# This script initializes resources before using Terraform.
# Pass the project_id and a subfolder path (e.g., gcp/apis).

export PROJECT_ID=$(gcloud info --format='value(config.project)')

# Extract the last segment of the subfolder path as PREFIX
if [ -z "$2" ]; then
    INIT_DIR="./gcp/init"
    PREFIX=""
    CONFIG_DIR="./gcp/config"
else
    INIT_DIR="./$2/init"
    PREFIX=$(basename "$2")
    CONFIG_DIR="./$2/config"
fi

BACKEND_FILE="$INIT_DIR/backend.tfvars"
TERRAFORM_BUCKET=$PROJECT_ID-niflheim-tfstate

echo "******"
echo "ProjectID value: $PROJECT_ID"
echo "Backend terraform bucket: $TERRAFORM_BUCKET"
echo "******"
echo "GCP basic APIs activation: "
echo "serviceusage.googleapis.com, "
echo "cloudresourcemanager.googleapis.com, "
echo "cloudbuild.googleapis.com, "
echo "artifactregistry.googleapis.com"
echo "******"

# Create the GCS bucket if it doesn't exist and enable versioning
gsutil ls -b -p $PROJECT_ID gs://$TERRAFORM_BUCKET || gsutil mb -l eu -p $PROJECT_ID gs://$TERRAFORM_BUCKET || gsutil versioning set on gs://$TERRAFORM_BUCKET

# Create init folder if it doesn't exist
mkdir -p $INIT_DIR

# Create the config folder if it doesn't exist and add the variables.tfvars file
mkdir -p $CONFIG_DIR
echo "project_id = \"$PROJECT_ID\"" > $CONFIG_DIR/variables.tfvars

# Write the backend.tfvars file in the correct location
echo "bucket = \"$TERRAFORM_BUCKET\"" > $BACKEND_FILE
if [ -n "$PREFIX" ]; then
    echo "prefix = \"$PREFIX\"" >> $BACKEND_FILE
fi

echo "Backend tfvars file created at: $BACKEND_FILE"
echo "******"

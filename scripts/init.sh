#!/bin/bash

# This script initializes resources before using Terraform.
# Pass the project_id and a subfolder path (e.g., gcp/apis).

export PROJECT_ID=$(gcloud info --format='value(config.project)')

# Extract the last segment of the subfolder path as PREFIX
if [ "$2" == "gcp" ]; then
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

# Create the GCS bucket if it doesn't exist and enable versioning
gsutil ls -b -p $PROJECT_ID gs://$TERRAFORM_BUCKET || gsutil mb -l eu -p $PROJECT_ID gs://$TERRAFORM_BUCKET || gsutil versioning set on gs://$TERRAFORM_BUCKET

# Create init folder if it doesn't exist
mkdir -p $INIT_DIR

# Create the config folder if it doesn't exist and add the variables.tfvars file
mkdir -p $CONFIG_DIR
# Create the variables.tfvars file if it doesn't exist
if [ ! -f "$CONFIG_DIR/variable.tfvars" ]; then
    touch $CONFIG_DIR/variable.tfvars
    echo "project_id = \"$PROJECT_ID\"" > $CONFIG_DIR/variable.tfvars
    echo "region = \"europe-west1\"" >> $CONFIG_DIR/variable.tfvars
fi

# Write the backend.tfvars file in the correct location
echo "bucket = \"$TERRAFORM_BUCKET\"" > $BACKEND_FILE
if [ -n "$PREFIX" ]; then
    echo "prefix = \"$PREFIX\"" >> $BACKEND_FILE
fi

echo "Backend tfvars file created at: $BACKEND_FILE"
echo "******"

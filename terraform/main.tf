# main.tf

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"  # Specify the provider version you want
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file(var.credentials)  # Uses the path specified in variables.tf
}

resource "google_storage_bucket" "crypto_data_bucket" {
  name                        = var.bucket_name
  location                    = var.region
  force_destroy               = true  # Allows bucket to be deleted even if it contains objects
  storage_class               = "STANDARD"  # You can change this to your preferred storage class
  uniform_bucket_level_access = true  # Enables uniform access controls

  versioning {
    enabled = true  # Enables versioning for the bucket
  }

  lifecycle_rule {
    action {
      type = "Delete"  # Action to take on lifecycle rule
    }

    condition {
      age = 21  # Deletes objects older than 21 days
    }
  }
}

resource "google_bigquery_dataset" "cryptocurrency_insights" {
  dataset_id = "cryptocurrency_insights"  # ID for the BigQuery dataset
  project    = var.project_id  # Uses the project ID variable
}

output "bucket_name" {
  value = google_storage_bucket.crypto_data_bucket.name  # Outputs the bucket name after creation
}

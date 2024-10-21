# variables.tf

variable "credentials" {
  default     = "/mnt/c/Users/Dina Galevska/course_project/cryptocurrency-insights/keys/service-account-key.json"
  description = "Path to Google Credentials"
}

variable "project_id" {
  default     = "cryptomarketdashboard" 
  description = "GCP Project ID"
}

variable "region" {
  default     = "europe-central2"  
  description = "Region for GCP resources"
}

variable "bucket_name" {
  default     = "crypto-data-bucket-002" 
  description = "Name of the Google Cloud Storage bucket"
}

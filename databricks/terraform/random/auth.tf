variable "databricks_connection_profile" {}

terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {}

# Use Databricks CLI authentication.
provider "databricks" {
  profile = var.databricks_connection_profile
}

terraform {
  required_providers {
    databricks = {
      source   = "databricks/databricks"
    }
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region     = var.region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key  
  default_tags {
    tags = merge(var.tags, {
    Owner = var.resource_owner
    Resource = var.resource_prefix
    })
  }
}

provider "databricks" {
  alias     = "mws"
  host      = "https://accounts.cloud.databricks.com"
  client_id     = var.databricks_service_principle_client_id
  client_secret = var.databricks_service_principle_client_secret
  account_id    = var.databricks_account_id
}


provider "databricks" {
  alias     = "created_workspace"
  host      = module.databricks_mws_workspace.workspace_url
  client_id     = var.databricks_service_principle_client_id
  client_secret = var.databricks_service_principle_client_secret
  account_id    = var.databricks_account_id
}
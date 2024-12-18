variable "databricks_account_client_id" {
  type        = string
  description = "Application ID of account-level service principal"
}

variable "databricks_account_client_secret" {
  type        = string
  description = "Client secret of account-level service principal"
}

variable "databricks_account_id" {
  type        = string
  description = "Databricks Account ID"
}

variable "aws_account_id" {
  type        = string
  description = "(Required) AWS account ID where the cross-account role for Unity Catalog will be created"
}

variable "region" {
  type        = string
  description = "AWS region to deploy to"
  default     = "us-east-2"
}

variable "tags" {
  default     = {"origin": "analytics-databricks-stage-2"}
  type        = map(string)
  description = "Optional tags to add to created resources"
}

variable "databricks_workspace_ids" {
  description = <<EOT
  List of Databricks workspace IDs to be enabled with Unity Catalog.
  Enter with square brackets and double quotes
  e.g. ["111111111", "222222222"]
  EOT
  type        = list(string)
  default     = ["2424101092929547"]
}

variable "databricks_users" {
  description = <<EOT
  List of Databricks users to be added at account-level for Unity Catalog. should we put the account owner email here? maybe not since it's always there and we dont want tf to destroy
  Enter with square brackets and double quotes
  e.g ["first.last@domain.com", "second.last@domain.com"]
  EOT
  type        = list(string)
}


variable "databricks_account_admins" {
  description = <<EOT
  List of Admins to be added at account-level for Unity Catalog.
  Enter with square brackets and double quotes
  e.g ["first.admin@domain.com", "second.admin@domain.com"]
  EOT
  type        = list(string)
}

variable "unity_admin_group" {
  description = "Name of the admin group. This group will be set as the owner of the Unity Catalog metastore"
  type        = string
}

variable "pat_ws_1" {
  type      = string
  sensitive = true
}

variable "pat_ws_2" {
  type      = string
  sensitive = true
}
variable "databricks_account_username" {
  type = string
  sensitive = true
}

variable "databricks_account_password" {
  type = string
  sensitive = true
}

variable "databricks_account_id" {
  type = string
  sensitive = true
}

variable "aws_access_key" {
  type = string
  sensitive = true
}

variable "aws_secret_key" {
  type = string
  sensitive = true
}

variable "aws_account_id" {
  type = string
}

variable "curated_data_bucket" {
  type = string
}

variable "wrangled_data_bucket" {
  type = string
}

variable "archive_data_bucket" {
  type = string
}

variable "data_bucket" {
  type = string
}

variable "resource_owner" {
  type = string
  sensitive = true
}

variable "region" {
  type = string
}

variable "vpc_cidr_range" {
  type = string
}

variable "private_subnets_cidr" {
  type = string
}

variable "public_subnets_cidr" {
  type = string
}

variable "privatelink_subnets_cidr" {
  type = string
}

variable "availability_zones" {
  type = string
}

variable "workspace_vpce_service" {
  type = string
  default = ""
}

variable "relay_vpce_service" {
  type = string
  default = ""
}

variable "tags" {
  default = {"origin": "analytics-databricks"}
}

variable "resource_prefix" {
  type = string
}

variable "databricks_de_users" {
  type = list(string)
}
variable "databricks_ds_users" {
  type = list(string)
}
variable "databricks_da_users" {
  type = list(string)
}

variable "databricks_users" {
  description = <<EOT
  List of Databricks users to be added at account-level for Unity Catalog.
  Enter with square brackets and double quotes
  e.g ["first.last@domain.com", "second.last@domain.com"]
  EOT
  type        = list(string)
}

variable "databricks_metastore_admins" {
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
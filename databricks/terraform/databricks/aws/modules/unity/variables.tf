variable "resource_prefix" {
  type = string
}

variable "databricks_workspace" {
  type = string
}

variable "uc_s3" {
  type = string
}

variable "uc_iam_arn" {
  type = string
}

variable "uc_iam_name" {
  type = string
}

variable "data_bucket" {
  type = string
}

variable "storage_credential_role_name" {
  type = string
}

variable "storage_credential_role_arn" {
  type = string
}

# variable "databricks_de_users" {
#   type = list(string)
# }
# variable "databricks_ds_users" {
#   type = list(string)
# }
# variable "databricks_da_users" {
#   type = list(string)
# }

# variable "databricks_users" {
#   description = <<EOT
#   List of Databricks users to be added at account-level for Unity Catalog.
#   Enter with square brackets and double quotes
#   e.g ["first.last@domain.com", "second.last@domain.com"]
#   EOT
#   type        = list(string)
# }

# variable "databricks_metastore_admins" {
#   description = <<EOT
#   List of Admins to be added at account-level for Unity Catalog.
#   Enter with square brackets and double quotes
#   e.g ["first.admin@domain.com", "second.admin@domain.com"]
#   EOT
#   type        = list(string)
# }

# variable "unity_admin_group" {
#   description = "Name of the admin group. This group will be set as the owner of the Unity Catalog metastore"
#   type        = string
# }


variable "de_user_group" {
  type = string
}

variable "ds_user_group" {
  type = string
}

variable "da_user_group" {
  type = string
}

variable "curated_external_bucket" {
  type = string
}

variable "iam_external_curated_arn" {
  type = string
}

variable "wrangled_external_bucket" {
  type = string
}

variable "iam_external_wrangled_arn" {
  type = string
}

variable "archive_external_bucket" {
  type = string
}

variable "iam_external_archive_arn" {
  type = string
}

variable "aws_account_id" {
  type = string
}
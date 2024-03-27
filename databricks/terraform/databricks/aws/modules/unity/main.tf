# Metastore
resource "databricks_metastore" "this" {
  name          = "unity-catalog-${var.resource_prefix}"
  storage_root  = "s3://${var.uc_s3}/metastore"
  force_destroy = true
}

resource "databricks_metastore_assignment" "default_metastore" {
  workspace_id         = var.databricks_workspace
  metastore_id         = databricks_metastore.this.id
  default_catalog_name = "hive_metastore"
}

resource "databricks_metastore_data_access" "this" {
  metastore_id = databricks_metastore.this.id
  name         = var.uc_iam_name
  aws_iam_role {
    role_arn = var.uc_iam_arn
  }
  is_default = true
  depends_on = [
    databricks_metastore_assignment.default_metastore
  ]
}

// -------------------------------------------- 

# Curated External Storage Credential
resource "databricks_storage_credential" "curated_external_bucket" {
  name     = var.curated_external_bucket
  aws_iam_role {
    role_arn = var.iam_external_curated_arn
  }
  comment = "Managed by TF - curated external storage"
}

resource "databricks_external_location" "curated_external_bucket" {
  name            = "curated_external_bucket"
  url             = "s3://${var.curated_external_bucket}/"
  credential_name = databricks_storage_credential.curated_external_bucket.id
  comment         = "Managed by TF - curated external storage"
}

resource "databricks_grants" "curated_external_creds" {
  storage_credential = databricks_storage_credential.curated_external_bucket.id
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Scientists"
    privileges = ["CREATE_TABLE", "READ_FILES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["READ_FILES"]
  }
}



# Wrangled External Storage Credential
resource "databricks_storage_credential" "wrangled_external_bucket" {
  name     = var.wrangled_external_bucket
  aws_iam_role {
    role_arn = var.iam_external_wrangled_arn
  }
  comment = "Managed by TF - wrangled external storage"
}

resource "databricks_external_location" "wrangled_external_bucket" {
  name            = "wrangled_external_bucket"
  url             = "s3://${var.wrangled_external_bucket}/"
  credential_name = databricks_storage_credential.wrangled_external_bucket.id
  comment         = "Managed by TF - wrangled external storage"
}

resource "databricks_grants" "wrangled_external_creds" {
  storage_credential = databricks_storage_credential.wrangled_external_bucket.id
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Scientists"
    privileges = ["CREATE_TABLE", "READ_FILES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["READ_FILES"]
  }
}


# Archive External Storage Credential
resource "databricks_storage_credential" "archive_external_bucket" {
  name     = var.archive_external_bucket
  aws_iam_role {
    role_arn = var.iam_external_archive_arn
  }
  comment = "Managed by TF - archive external storage"
}

resource "databricks_external_location" "archive_external_bucket" {
  name            = "archive_external_bucket"
  url             = "s3://${var.archive_external_bucket}/"
  credential_name = databricks_storage_credential.archive_external_bucket.id
  comment         = "Managed by TF - archive external storage"
}

resource "databricks_grants" "archive_external_creds" {
  storage_credential = databricks_storage_credential.archive_external_bucket.id
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Scientists"
    privileges = ["READ_FILES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["READ_FILES"]
  }
}



# CATALOGS =============================================================================================================================================================================================

# SCHEMAS =============================================================================================================================================================================================

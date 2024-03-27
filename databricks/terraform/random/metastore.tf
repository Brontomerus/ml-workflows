resource "databricks_metastore" "this" {
  name          = "primary"
  storage_root  = "s3://btd-analytics-etl/metastore"
  owner         = "btd admins"
  force_destroy = true
}

resource "databricks_metastore_assignment" "this" {
  metastore_id = databricks_metastore.this.id
  workspace_id = local.workspace_id
}

resource "databricks_catalog" "btd-ml-workflows" {
  metastore_id = databricks_metastore.this.id
  name         = "btd-ml-workflows"
  comment      = "this catalog is managed by terraform in the btd-data repository"
  properties = {
    purpose = "data governance"
  }
}
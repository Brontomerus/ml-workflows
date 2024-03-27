# ====================================== master_data ======================================
resource "databricks_catalog" "master_data" {
  metastore_id = databricks_metastore.this.id
  name         = "master_data"
  comment      = "Master Data such as key dimensions and utilities"
  properties = {
    purpose = "analytics"
  }
  depends_on = [databricks_metastore_assignment.default_metastore]
}

resource "databricks_grants" "master_data" {
  catalog  = databricks_catalog.master_data.name
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
}

# ====================================== economy ======================================
resource "databricks_catalog" "economy" {
  metastore_id = databricks_metastore.this.id
  name         = "economy"
  comment      = "catalog for resources used with economies"
  properties = {
    purpose = "analytics"
  }
  depends_on = [databricks_metastore_assignment.default_metastore]
}

resource "databricks_grants" "economy" {
  catalog  = databricks_catalog.economy.name
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
}

# ====================================== api ======================================
resource "databricks_catalog" "api" {
  metastore_id = databricks_metastore.this.id
  name         = "api"
  comment      = "Data for managing API resources"
  properties = {
    purpose = "analytics"
  }
  depends_on = [databricks_metastore_assignment.default_metastore]
}

resource "databricks_grants" "api" {
  catalog  = databricks_catalog.api.name
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
}

# ====================================== engagement ======================================
resource "databricks_catalog" "engagement" {
  metastore_id = databricks_metastore.this.id
  name         = "engagement"
  comment      = "catalog for engagement metrics and resources"
  properties = {
    purpose = "analytics"
  }
  depends_on = [databricks_metastore_assignment.default_metastore]
}

resource "databricks_grants" "engagement" {
  catalog  = databricks_catalog.engagement.name
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
}

# ====================================== bi ======================================
resource "databricks_catalog" "bi" {
  metastore_id = databricks_metastore.this.id
  name         = "bi"
  comment      = "catalog for business intelligence reporting needs"
  properties = {
    purpose = "analytics"
  }
  depends_on = [databricks_metastore_assignment.default_metastore]
}

resource "databricks_grants" "bi" {
  catalog  = databricks_catalog.bi.name
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
}


# ====================================== egress ======================================
resource "databricks_catalog" "egress" {
  metastore_id = databricks_metastore.this.id
  name         = "egress"
  comment      = "catalog to manage egress data"
  properties = {
    purpose = "analytics"
  }
  depends_on = [databricks_metastore_assignment.default_metastore]
}

resource "databricks_grants" "egress" {
  catalog  = databricks_catalog.egress.name
  grant {
    principal  = "Data Scientists"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
}

# ====================================== sandbox ======================================
resource "databricks_catalog" "sandbox" {
  metastore_id = databricks_metastore.this.id
  name         = "sandbox"
  comment      = "adhoc data exploration"
  properties = {
    purpose = "analytics"
  }
  depends_on = [databricks_metastore_assignment.default_metastore]
}

resource "databricks_grants" "sandbox" {
  catalog  = databricks_catalog.sandbox.name
  grant {
    principal  = "Data Scientists"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["ALL_PRIVILEGES"]
  }
}

# ====================================== wrangled ======================================
resource "databricks_catalog" "wrangled" {
  metastore_id = databricks_metastore.this.id
  name         = "wrangled"
  comment      = "wrangled, cleansing, and staging data in data pipelines"
  properties = {
    purpose = "analytics etl"
  }
  depends_on = [databricks_metastore_assignment.default_metastore]
}

resource "databricks_grants" "wrangled" {
  catalog  = databricks_catalog.wrangled.name
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
}

# ====================================== utility ======================================
resource "databricks_catalog" "utility" {
  metastore_id = databricks_metastore.this.id
  name         = "utility"
  comment      = "utility and operations uses"
  properties = {
    purpose = "analytics etl"
  }
  depends_on = [databricks_metastore_assignment.default_metastore]
}

resource "databricks_grants" "utility" {
  catalog  = databricks_catalog.utility.name
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA", "USE_CATALOG", "SELECT", "EXECUTE"]
  }
}

# ====================================== master_data.system ======================================
resource "databricks_schema" "system" {
  catalog_name = databricks_catalog.master_data.id
  name         = "system"
  comment      = "master information regarding external and internal systems and utilities"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "system" {
  schema   = databricks_schema.system.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== master_data.app ======================================
resource "databricks_schema" "app" {
  catalog_name = databricks_catalog.master_data.id
  name         = "app"
  comment      = "Cataloging application information"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "app" {
  schema   = databricks_schema.app.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== master_data.tests ======================================
resource "databricks_schema" "tests" {
  catalog_name = databricks_catalog.master_data.id
  name         = "tests"
  comment      = "Information regarding modeling and multivariat testing"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "tests" {
  schema   = databricks_schema.tests.id
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
    privileges = ["USE_SCHEMA"]
  }
}


# ====================================== master_data.mappers ======================================
resource "databricks_schema" "mappers" {
  catalog_name = databricks_catalog.master_data.id
  name         = "mappers"
  comment      = "mappers and resources for broad use with other data domains"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "mappers" {
  schema   = databricks_schema.mappers.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== master_data.dimensions ======================================
resource "databricks_schema" "dimensions" {
  catalog_name = databricks_catalog.master_data.id
  name         = "dimensions"
  comment      = "dimensions such as location and app types"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "dimensions" {
  schema   = databricks_schema.dimensions.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== economy.iap ======================================
resource "databricks_schema" "iap" {
  catalog_name = databricks_catalog.economy.id
  name         = "iap"
  comment      = "In App Purchase Data"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "iap" {
  schema   = databricks_schema.iap.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== economy.monetization ======================================
resource "databricks_schema" "monetization" {
  catalog_name = databricks_catalog.economy.id
  name         = "monetization"
  comment      = "Monetization Data: Ads, Puchases, etc"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "monetization" {
  schema   = databricks_schema.monetization.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}


# ====================================== economy.modeling ======================================
resource "databricks_schema" "modeling" {
  catalog_name = databricks_catalog.economy.id
  name         = "modeling"
  comment      = "In App Purchase Data"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "modeling" {
  schema   = databricks_schema.modeling.id
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
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== economy.progression ======================================
resource "databricks_schema" "progression" {
  catalog_name = databricks_catalog.economy.id
  name         = "progression"
  comment      = "Levels and progression information such as xp and other resources"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "progression" {
  schema   = databricks_schema.progression.id
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

# ====================================== economy.rewards ======================================
resource "databricks_schema" "rewards" {
  catalog_name = databricks_catalog.economy.id
  name         = "rewards"
  comment      = "Rewards information for application specials and other promos"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "rewards" {
  schema   = databricks_schema.rewards.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== economy.store ======================================
resource "databricks_schema" "store" {
  catalog_name = databricks_catalog.economy.id
  name         = "store"
  comment      = "Store data like pricing, promos, and other information regarding in app purchase data"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "store" {
  schema   = databricks_schema.store.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== api.services ======================================
resource "databricks_schema" "services" {
  catalog_name = databricks_catalog.api.id
  name         = "services"
  comment      = "Information regarding api services and functionalities"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "services" {
  schema   = databricks_schema.services.id
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

# ====================================== api.usage ======================================
resource "databricks_schema" "usage" {
  catalog_name = databricks_catalog.api.id
  name         = "usage"
  comment      = "Information regarding api service usage"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "usage" {
  schema   = databricks_schema.usage.id
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
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== bi.reports ======================================
resource "databricks_schema" "reports" {
  catalog_name = databricks_catalog.bi.id
  name         = "reports"
  comment      = "Information regarding business intelligence service reports"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "reports" {
  schema   = databricks_schema.reports.id
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

# ====================================== bi.mart ======================================
resource "databricks_schema" "mart" {
  catalog_name = databricks_catalog.bi.id
  name         = "mart"
  comment      = "Data model to serve business intelligence service bi tools"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "mart" {
  schema   = databricks_schema.mart.id
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

# ====================================== engagement.metrics ======================================
resource "databricks_schema" "metrics" {
  catalog_name = databricks_catalog.engagement.id
  name         = "metrics"
  comment      = "Database for engagement metrics"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "metrics" {
  schema   = databricks_schema.metrics.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== engagement.events ======================================
resource "databricks_schema" "events" {
  catalog_name = databricks_catalog.engagement.id
  name         = "events"
  comment      = "database for user events and accumulator data collected from client sources like google analytics"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "events" {
  schema   = databricks_schema.events.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== engagement.users ======================================
resource "databricks_schema" "engagement_users" {
  catalog_name = databricks_catalog.engagement.id
  name         = "users"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "engagement_users" {
  schema   = databricks_schema.engagement_users.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== egress.reporting ======================================
resource "databricks_schema" "reporting" {
  catalog_name = databricks_catalog.egress.id
  name         = "reporting"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "reporting" {
  schema   = databricks_schema.reporting.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== egress.partner ======================================
resource "databricks_schema" "partner" {
  catalog_name = databricks_catalog.egress.id
  name         = "partner"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "partner" {
  schema   = databricks_schema.partner.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== sandbox.data_science ======================================
resource "databricks_schema" "data_science" {
  catalog_name = databricks_catalog.sandbox.id
  name         = "data_science"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "data_science" {
  schema   = databricks_schema.data_science.id
  grant {
    principal  = "Data Scientists"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
}

# ====================================== sandbox.data_analytics ======================================
resource "databricks_schema" "data_analytics" {
  catalog_name = databricks_catalog.sandbox.id
  name         = "data_analytics"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "data_analytics" {
  schema   = databricks_schema.data_analytics.id
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

# ====================================== wrangled.raw ======================================
resource "databricks_schema" "raw" {
  catalog_name = databricks_catalog.wrangled.id
  name         = "raw"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "raw" {
  schema   = databricks_schema.raw.id
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
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== wrangled.staging ======================================
resource "databricks_schema" "staging" {
  catalog_name = databricks_catalog.wrangled.id
  name         = "staging"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "staging" {
  schema   = databricks_schema.staging.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== wrangled.engagement ======================================
resource "databricks_schema" "wrangled_engagement" {
  catalog_name = databricks_catalog.wrangled.id
  name         = "engagement"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "wrangled_engagement" {
  schema   = databricks_schema.wrangled_engagement.id
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
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== wrangled.bi ======================================
resource "databricks_schema" "wrangled_bi" {
  catalog_name = databricks_catalog.wrangled.id
  name         = "bi"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "wrangled_bi" {
  schema   = databricks_schema.wrangled_bi.id
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


# ====================================== wrangled.api ======================================
resource "databricks_schema" "wrangled_api" {
  catalog_name = databricks_catalog.wrangled.id
  name         = "api"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "wrangled_api" {
  schema   = databricks_schema.wrangled_api.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== wrangled.master_data ======================================
resource "databricks_schema" "wrangled_master_data" {
  catalog_name = databricks_catalog.wrangled.id
  name         = "master_data"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "wrangled_master_data" {
  schema   = databricks_schema.wrangled_master_data.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== wrangled.economy ======================================
resource "databricks_schema" "wrangled_economy" {
  catalog_name = databricks_catalog.wrangled.id
  name         = "economy"
  comment      = "this database is managed by terraform"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "wrangled_economy" {
  schema   = databricks_schema.wrangled_economy.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== wrangled.extracts ======================================
resource "databricks_schema" "extracts" {
  catalog_name = databricks_catalog.wrangled.id
  name         = "extracts"
  comment      = "historic data from the standalone archived application data"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "extracts" {
  schema   = databricks_schema.extracts.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== utility.orchestration ======================================
resource "databricks_schema" "orchestration" {
  catalog_name = databricks_catalog.utility.id
  name         = "orchestration"
  comment      = "utility orchestration information"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "orchestration" {
  schema   = databricks_schema.orchestration.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== utility.tools ======================================
resource "databricks_schema" "tools" {
  catalog_name = databricks_catalog.utility.id
  name         = "tools"
  comment      = "system tools schema for misc processes and functionalities"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "tools" {
  schema   = databricks_schema.tools.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}

# ====================================== api.internal ======================================
resource "databricks_schema" "internal" {
  catalog_name = databricks_catalog.api.id
  name         = "internal"
  comment      = "internal api requirements and tooling"
  properties = {
    kind = "various"
  }
}

resource "databricks_grants" "internal" {
  schema   = databricks_schema.internal.id
  grant {
    principal  = "Data Scientists"
    privileges = ["USE_SCHEMA"]
  }
  grant {
    principal  = "Data Engineers"
    privileges = ["ALL_PRIVILEGES"]
  }
  grant {
    principal  = "Data Analysts"
    privileges = ["USE_SCHEMA"]
  }
}
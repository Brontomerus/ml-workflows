resource "databricks_secret_scope" "this" {
  name = "demo-${data.databricks_current_user.me.alphanumeric}"
}

resource "databricks_token" "pat" {
  comment          = "Created from ${abspath(path.module)}"
  lifetime_seconds = 3600
}

resource "databricks_secret" "token" {
  string_value = databricks_token.pat.token_value
  scope        = databricks_secret_scope.this.name
  key          = "token"
}

resource "databricks_notebook" "this" {
  path     = "${data.databricks_current_user.me.home}/Terraform"
  language = "PYTHON"
  content_base64 = base64encode(<<-EOT
    token = dbutils.secrets.get('${databricks_secret_scope.this.name}', '${databricks_secret.token.key}')
    print(f'This should be redacted: {token}')
    EOT
  )
}

resource "databricks_job" "this" {
  name = "Terraform Demo (${data.databricks_current_user.me.alphanumeric})"

  new_cluster {
    num_workers   = 1
    spark_version = data.databricks_spark_version.latest.id
    node_type_id  = data.databricks_node_type.smallest.id
  }

  notebook_task {
    notebook_path = databricks_notebook.this.path
  }
}

resource "databricks_cluster" "this" {
  cluster_name            = "Exploration (${data.databricks_current_user.me.alphanumeric})"
  spark_version           = data.databricks_spark_version.latest.id
  instance_pool_id        = databricks_instance_pool.smallest_nodes.id
  autotermination_minutes = 15
  autoscale {
    min_workers = 0
    max_workers = 6
  }
}

resource "databricks_cluster_policy" "this" {
  name = "Minimal (${data.databricks_current_user.me.alphanumeric})"
  definition = jsonencode({
    "dbus_per_hour" : {
      "type" : "range",
      "maxValue" : 8
    },
    "autotermination_minutes" : {
      "type" : "fixed",
      "value" : 15,
      "hidden" : true
    }
  })
}

resource "databricks_instance_pool" "smallest_nodes" {
  instance_pool_name = "Smallest Nodes (${data.databricks_current_user.me.alphanumeric})"
  min_idle_instances = 0
  max_capacity       = 6
  node_type_id       = data.databricks_node_type.smallest.id
  preloaded_spark_versions = [
    data.databricks_spark_version.latest.id
  ]

  idle_instance_autotermination_minutes = 15
}

output "notebook_url" {
  value = databricks_notebook.this.url
}

output "job_url" {
  value = databricks_job.this.url
}

# ================================================================== Security ================================================================================
resource "databricks_secret_acl" "spectators" {
  principal  = databricks_group.spectators.display_name
  scope      = databricks_secret_scope.this.name
  permission = "READ"
}

resource "databricks_group" "spectators" {
  display_name = "Spectators (by ${data.databricks_current_user.me.alphanumeric})"
}

resource "databricks_user" "brandon" {
  user_name    = "brandon+${data.databricks_current_user.me.alphanumeric}@example.com"
  display_name = "Brandon ${data.databricks_current_user.me.alphanumeric}"
}

resource "databricks_group_member" "alpha" {
  group_id  = databricks_group.spectators.id
  member_id = databricks_user.brandon.id
}

resource "databricks_permissions" "notebook" {
  notebook_path = databricks_notebook.this.id
  access_control {
    user_name        = databricks_user.brandon.user_name
    permission_level = "CAN_RUN"
  }
  access_control {
    group_name       = databricks_group.spectators.display_name
    permission_level = "CAN_READ"
  }
}

resource "databricks_permissions" "job" {
  job_id = databricks_job.this.id
  access_control {
    user_name        = databricks_user.brandon.user_name
    permission_level = "IS_OWNER"
  }
  access_control {
    group_name       = databricks_group.spectators.display_name
    permission_level = "CAN_MANAGE_RUN"
  }
}

resource "databricks_permissions" "cluster" {
  cluster_id = databricks_cluster.this.id
  access_control {
    user_name        = databricks_user.brandon.user_name
    permission_level = "CAN_RESTART"
  }
  access_control {
    group_name       = databricks_group.spectators.display_name
    permission_level = "CAN_ATTACH_TO"
  }
}

resource "databricks_permissions" "policy" {
  cluster_policy_id = databricks_cluster_policy.this.id
  access_control {
    group_name       = databricks_group.spectators.display_name
    permission_level = "CAN_USE"
  }
}

resource "databricks_permissions" "pool" {
  instance_pool_id = databricks_instance_pool.smallest_nodes.id
  access_control {
    group_name       = databricks_group.spectators.display_name
    permission_level = "CAN_ATTACH_TO"
  }
}
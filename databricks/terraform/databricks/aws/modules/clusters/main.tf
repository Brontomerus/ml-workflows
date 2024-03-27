# Account Instance Profile 
resource "databricks_instance_profile" "shared" {
  instance_profile_arn = var.instance_profile
}

# DE + ML Cluster
data "databricks_spark_version" "latest_lts" {
  long_term_support = true
  # provider          = databricks.workspace
}

data "databricks_node_type" "smallest" {
  # provider   = databricks.workspace
  local_disk = true
}

resource "databricks_cluster" "unity_shared_autoscaling" {
  cluster_name              = "Unity Shared Autoscaling"
  spark_version             = data.databricks_spark_version.latest_lts.id
  node_type_id              = data.databricks_node_type.smallest.id
  # node_type_id              = "i3.xlarge"
  enable_elastic_disk       = false
  autotermination_minutes   = 15
  data_security_mode        = "USER_ISOLATION"
  autoscale {
    min_workers = 0
    max_workers = 6
  }
  aws_attributes {
    instance_profile_arn    = var.instance_profile
    availability            = "SPOT"
    zone_id                 = "auto"
  }
  depends_on = [
    databricks_instance_profile.shared
  ]
}

resource "databricks_cluster" "unity_autoscaling_admin" {
  cluster_name              = "Admin Unity Autoscaling"
  spark_version             = data.databricks_spark_version.latest_lts.id
  # node_type_id              = data.databricks_node_type.smallest.id
  node_type_id              = "i3.xlarge"
  enable_elastic_disk       = false
  autotermination_minutes   = 15
  num_workers               = 2
  data_security_mode        = "SINGLE_USER"
  single_user_name          = "brandon.donelan@outlook.com"
  autoscale {
    min_workers = 0
    max_workers = 4
  }
  aws_attributes {
    instance_profile_arn    = var.instance_profile
    availability            = "SPOT_WITH_FALLBACK"
    zone_id                 = "auto"
    first_on_demand         = 1
    spot_bid_price_percent  = 100
  }
  depends_on = [
    databricks_instance_profile.shared
  ]
}


resource "databricks_cluster" "single_node" {
  cluster_name            = "Single Node"
  spark_version           = data.databricks_spark_version.latest_lts.id
  node_type_id            = data.databricks_node_type.smallest.id
  autotermination_minutes = 20
  num_workers             = 0
  aws_attributes {
    instance_profile_arn    = var.instance_profile
    availability            = "SPOT"
    zone_id                 = "auto"
  }
  spark_conf = {
    # Single-node
    "spark.databricks.cluster.profile" : "singleNode"
    "spark.master" : "local[*]"
  }
  custom_tags = {
    "ResourceClass" = "SingleNode"
  }
  depends_on = [
    databricks_instance_profile.shared
  ]
}

resource "databricks_cluster" "unity_single_node_admin" {
  cluster_name            = "Unity Single Node"
  spark_version           = data.databricks_spark_version.latest_lts.id
  node_type_id            = data.databricks_node_type.smallest.id
  autotermination_minutes = 10
  enable_elastic_disk     = false
  num_workers             = 0
  aws_attributes {
    instance_profile_arn    = var.instance_profile
    availability            = "SPOT"
    zone_id                 = "auto"
  }
  data_security_mode = "SINGLE_USER"
  single_user_name   = "brandon.donelan@outlook.com"
  spark_conf = {
    # Single-node
    "spark.databricks.cluster.profile" : "singleNode"
    "spark.master" : "local[*]"
  }
  custom_tags = {
    "ResourceClass" = "SingleNode"
  }
  depends_on = [
    databricks_instance_profile.shared
  ]
}




# data "databricks_group" "data_eng_clusters" {
#   display_name = "Data Engineering Clusters"
# }

# data "databricks_user" "data_eng_clusters" {
#   for_each = data.databricks_group.data_eng_clusters.members
#   user_id  = each.key
# }



# resource "databricks_cluster" "unity_data_engineering_autoscale" {
#   for_each                = databricks_user.data_engineer_users
#   cluster_name            = "${each.value.display_name} unity data engineering"
#   spark_version           = data.databricks_spark_version.latest_lts.id
#   node_type_id            = data.databricks_node_type.smallest.id
#   enable_elastic_disk     = false
#   autotermination_minutes = 10
#   autoscale {
#     min_workers = 0
#     max_workers = 6
#   }
#   aws_attributes {
#     instance_profile_arn    = var.instance_profile
#     availability            = "SPOT"
#     zone_id                 = "auto"
#   }
#   depends_on = [
#     databricks_instance_profile.shared
#   ]
#   data_security_mode = "SINGLE_USER"
#   single_user_name   = each.value.user_name
  
# }

# resource "databricks_permissions" "unity_data_engineering_autoscale_restart" {
#   for_each   = data.databricks_user.data_engineer_users
#   cluster_id = databricks_cluster.unity_data_engineering_autoscale[each.key].cluster_id
#   access_control {
#     user_name        = each.value.user_name
#     permission_level = "CAN_RESTART"
#   }
# }
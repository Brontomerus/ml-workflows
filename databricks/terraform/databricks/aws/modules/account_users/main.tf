resource "databricks_user" "unity_users" {
  for_each  = toset(concat(var.databricks_metastore_admins))
  user_name = each.key
  force     = true
}

resource "databricks_group" "admin_group" {
  display_name = "unity-admin"
}

resource "databricks_group_member" "admin_group_member" {
  for_each  = toset(var.databricks_metastore_admins)
  group_id  = databricks_group.admin_group.id
  member_id = databricks_user.unity_users[each.value].id
}

# resource "databricks_user_role" "metastore_admin" {
#   for_each = toset(var.databricks_metastore_admins)
#   user_id  = databricks_user.unity_users[each.value].id
#   role     = "account_admin"
# }


# resource "databricks_user" "data_engineer_users" {
#   for_each  = toset(var.databricks_de_users)
#   user_name = each.key
#   force     = true
# }
resource "databricks_group" "data_engineers" {
  display_name = "Data Engineers"
}
# resource "databricks_group_member" "data_engineers_members" {
#   for_each  = toset(var.databricks_de_users)
#   group_id  = databricks_group.data_engineers.id
#   member_id = databricks_user.data_engineer_users[each.value].id
# }



# resource "databricks_user" "data_science_users" {
#   for_each  = toset(var.databricks_ds_users)
#   user_name = each.key
#   force     = true
# }
resource "databricks_group" "data_scientists" {
  display_name = "Data Scientists"
}
# resource "databricks_group_member" "data_scientists_members" {
#   for_each  = toset(var.databricks_ds_users)
#   group_id  = databricks_group.data_scientists.id
#   member_id = databricks_user.data_science_users[each.value].id
# }

# resource "databricks_user" "data_analysts_users" {
#   for_each  = toset(var.databricks_da_users)
#   user_name = each.key
#   force     = true
# }
resource "databricks_group" "data_analysts" {
  display_name = "Data Analysts"
}
# resource "databricks_group_member" "data_analysts_members" {
#   for_each  = toset(var.databricks_da_users)
#   group_id  = databricks_group.data_analysts.id
#   member_id = databricks_user.data_analysts_users[each.value].id
# }


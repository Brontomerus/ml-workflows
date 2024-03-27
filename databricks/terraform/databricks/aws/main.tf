locals {
  account_id                   = var.aws_account_id
  prefix                       = var.resource_prefix
  owner                        = var.resource_owner
  vpc_cidr_range               = var.vpc_cidr_range
  private_subnets_cidr         = split(",", var.private_subnets_cidr)
  public_subnets_cidr          = split(",", var.public_subnets_cidr)
  sg_egress_ports              = [443, 3306, 6666]
  sg_ingress_protocol          = ["tcp", "udp"]
  sg_egress_protocol           = ["tcp", "udp"]
  availability_zones           = split(",", var.availability_zones)
  dbfsname                     = join("", [local.prefix, "-", var.region, "-", "dbfsroot"]) 
  ucname                       = join("", [local.prefix, "-", var.region, "-", "uc"]) 
}


module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.70.0"
  name                  = local.prefix
  cidr                  = local.vpc_cidr_range
  # secondary_cidr_blocks = local.public_subnets_cidr
  azs                   = local.availability_zones
  tags                  = var.tags
  enable_dns_hostnames = true
  enable_nat_gateway   = true
  create_igw           = true
  public_subnets       = local.public_subnets_cidr
  private_subnets      = local.private_subnets_cidr
  default_security_group_egress = [{
    cidr_blocks = "0.0.0.0/0"
  }]
  default_security_group_ingress = [{
    description = "Allow all internal TCP and UDP"
    self        = true
  }]
}

resource "databricks_mws_networks" "this" {
  provider           = databricks.mws
  account_id         = var.databricks_account_id
  network_name       = "${local.prefix}-network"
  security_group_ids = [module.vpc.default_security_group_id]
  subnet_ids         = module.vpc.private_subnets
  vpc_id             = module.vpc.vpc_id
}


# Create External Databricks Workspace
module "databricks_mws_workspace" {
  source = "./modules/workspace"
  providers = {
    databricks = databricks.mws
  }
  databricks_account_id        = var.databricks_account_id
  resource_prefix              = local.prefix
  security_group_ids           = databricks_mws_networks.this.security_group_ids
  subnet_ids                   = databricks_mws_networks.this.subnet_ids
  vpc_id                       = databricks_mws_networks.this.vpc_id
  cross_account_role_arn       = aws_iam_role.cross_account_role.arn
  bucket_name                  = aws_s3_bucket.root_storage_bucket.id
  region                       = var.region
  # backend_rest                 = aws_vpc_endpoint.backend_rest.id
  # backend_relay                = aws_vpc_endpoint.backend_relay.id
}


# # Create Unity Catalog
# module "databricks_user_administration" {
#   source = "./modules/account_users"
#   providers = {
#     databricks = databricks.mws
#   }
#   databricks_de_users             = var.databricks_de_users
#   databricks_ds_users             = var.databricks_ds_users
#   databricks_da_users             = var.databricks_da_users
#   databricks_users                = var.databricks_users
#   databricks_metastore_admins     = var.databricks_metastore_admins
#   unity_admin_group               = var.unity_admin_group
#   databricks_workspace            = module.databricks_mws_workspace.workspace_id
# }

# Create Workspace Users
module "databricks_ws_user_administration" {
  source = "./modules/workspace_users"
  providers = {
    databricks = databricks.created_workspace
  }
  databricks_de_users             = var.databricks_de_users
  databricks_ds_users             = var.databricks_ds_users
  databricks_da_users             = var.databricks_da_users
  databricks_users                = var.databricks_users
  databricks_metastore_admins     = var.databricks_metastore_admins
  unity_admin_group               = var.unity_admin_group
  databricks_workspace            = module.databricks_mws_workspace.workspace_id
  depends_on                      = [module.databricks_mws_workspace]
}

# Create Unity Catalog
module "databricks_uc" {
    source = "./modules/unity"
    providers = {
      databricks = databricks.created_workspace
    }
  resource_prefix                 = local.prefix
  databricks_workspace            = module.databricks_mws_workspace.workspace_id
  uc_s3                           = aws_s3_bucket.unity_catalog_bucket.id
  uc_iam_arn                      = aws_iam_role.unity_catalog_role.arn
  uc_iam_name                     = aws_iam_role.unity_catalog_role.name
  data_bucket                     = var.data_bucket
  storage_credential_role_name    = aws_iam_role.storage_credential_role.name
  storage_credential_role_arn     = aws_iam_role.storage_credential_role.arn
  da_user_group                   = module.databricks_ws_user_administration.da_user_group
  ds_user_group                   = module.databricks_ws_user_administration.ds_user_group
  de_user_group                   = module.databricks_ws_user_administration.de_user_group
  curated_external_bucket         = var.curated_data_bucket
  iam_external_curated_arn        = aws_iam_role.external_curated_data_access_role.arn
  wrangled_external_bucket        = var.wrangled_data_bucket
  iam_external_wrangled_arn       = aws_iam_role.external_wrangled_data_access_role.arn
  archive_external_bucket         = var.archive_data_bucket
  iam_external_archive_arn        = aws_iam_role.external_archive_data_access_role.arn
  aws_account_id                  = var.aws_account_id
  depends_on                      = [module.databricks_mws_workspace, module.databricks_ws_user_administration]
}

# Create Create Cluster & Instance Profile
module "cluster_configuration" {
    source         = "./modules/clusters"
    providers      = {
      databricks   = databricks.created_workspace
    }
  instance_profile = aws_iam_instance_profile.s3_instance_profile.arn
  depends_on       = [module.databricks_mws_workspace]
}
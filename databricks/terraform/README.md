# Terraform: Infrastructure-as-Code
This directory holds are relevant terraform files to auto-generate much of the resources that are required to deploy resources for Databricks. Following the instructions and information in this README should enable you to successfully deploy this environment to the cloud platform of your choice. At the time of writing this documentation, only AWS Databricks is currently set up.

# Installing Terraform
to install Terraform onto your system, open this link in a browser and follow the instructions provided.

Link: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli



# Databricks
The Databricks Terraform can be found in `terraform/databricks/aws/*`, and will deploy the following resources given the correct input. Note that for VPC/Network configuration, this uses the default module for Databricks Workspace requirements, and is not customized. More information on this can be found at these links: [mws_vpc_endpoint](https://registry.terraform.io/providers/databricks/databricks/0.3.6/docs/resources/mws_vpc_endpoint) & [terraform-aws-modules](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)


### Additional information and useful links:
- https://docs.databricks.com/dev-tools/terraform/tutorial-aws.html
- https://docs.databricks.com/dev-tools/terraform/index.html
- https://registry.terraform.io/providers/databricks/databricks/latest/docs
- https://registry.terraform.io/providers/databricks/databricks/latest/docs/guides/unity-catalog
- https://docs.databricks.com/dev-tools/terraform/index.html



### AWS Resources:
- VPC & Subnets
- Networking Requirements Policies/Roles
- Databricks Workspace
- Databricks hive_metastore s3 bucket
- Unity Catalog s3 bucket
- External Storage s3 buckets for wrangled and curated zones
- IAM Roles/Polocies for access to encrypt/decrypt and access files in the s3 buckets
- Workspace Users
- Unity Catalog
- Unity Catalog Externail Storage Credentials
- Unity Catalog: Catalogs
- Unity Catalog: Schemas
- Unity Catalog: Permissions/Grants for Catalogs/Schemas
- Workspace Clusters: Shared Unity Autoscaling, Admin Unity Autoscaling, Single Node, Unity Single Node

<br>
<br>

*Note that you will want to create 3 groups in the Databricks Account portal prior to deployment:*
1. Data Engineers
2. Data Scientists
3. Data Analysts

## Installing Databricks Requirements
You will need to complete these steps prior to continuing, else you will be unable to execute the Terraform properly.

### 1. Setup databricks-cli:
You will need a python environment set up for this. If you don't know how thats done then oh boy are you up a creek without a paddle. More information can be found here: https://docs.databricks.com/dev-tools/cli/index.html#set-up-the-cli
```bash
pip install databricks-cli
```

### 2. Get a Databricks Access Token:
More information can be found here: https://docs.databricks.com/dev-tools/auth.html#personal-access-tokens-for-users

```bash
databricks configure --token
```

Test whether it worked:
```bash
databricks workspace ls /Users/
```

## variables.tfvars
This files will not appear if you cloned the repository from the remote origin due to the .gitignore file, so you will need to create this from scratch. Please Copy/Paste the following and fill the information out prior to continuing:
```sh
# Databricks Variables
databricks_account_username = ""
databricks_account_password = ""
databricks_account_id = ""
resource_owner = ""
resource_prefix = ""

# AWS Variables
aws_access_key = ""
aws_secret_key = ""
aws_account_id = ""
data_bucket = "analytics-btd-data-bucket"
curated_data_bucket = "analytics-btd-curated"
wrangled_data_bucket = "analytics-btd-wrangled"
archive_data_bucket = "btd-db-archive"

# Dataplane Variables
region = "us-east-1"
vpc_cidr_range = "10.0.0.0/18"
private_subnets_cidr = "10.0.32.0/26,10.0.32.64/26"
public_subnets_cidr = "10.0.16.0/22,10.0.24.0/22"
privatelink_subnets_cidr = "10.0.32.128/26,10.0.32.192/26"
availability_zones = "us-east-1a,us-east-1b"

# Not Required... Regional Private Link Variables: https://docs.databricks.com/administration-guide/cloud-configurations/aws/privatelink.html#regional-endpoint-reference
relay_vpce_service = ""
workspace_vpce_service = ""

databricks_users = ["",...]
databricks_metastore_admins = ["",...]
unity_admin_group = "unity-admin"

databricks_de_users = ["",...]
databricks_ds_users = ["",...]
databricks_da_users = ["",""]

```

## Executing Terraform

Once you have Terraform installed and prepared, as well as the `./databricks/aws/variables.tfvars` file completed, simply run each of these commands (optionally do not destroy the resources you create with that last command):
```bash
cd databricks/aws
terraform init
terraform plan -var-file ./variables.tfvars
terraform apply -var-file ./variables.tfvars
terraform destroy -var-file ./variables.tfvars
```


## Git Repository Integration
Once the workspace is deployed, follow these instructions to set up a git repository of your choice: https://docs.databricks.com/repos/get-access-tokens-from-git-provider.html



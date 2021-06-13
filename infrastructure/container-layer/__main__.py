"""An AWS Python Pulumi program"""
# REF: https://github.com/pulumi/examples/blob/master/aws-py-fargate/__main__.py

import json
import pulumi
import pulumi_aws as aws


# get configs defined in our yaml files
config = pulumi.Config()
network_layer_stack = config.require("network-layer-stack")
pulumi_account = config.require("user-account")


# get settings from stack references
env = pulumi.get_stack()
network_layer = pulumi.StackReference(f"{pulumi_account}/network-layer/{env}")


# Read back the project VPC and subnets id's that were set up in the network-layer-{env}, which we will use.
vpc_id = network_layer.require_output("vcp_id")
vpc_azs = network_layer.require_output("vpc_azs")
private_subnet_1_id = network_layer.require_output("private_subnet_1_id")
private_subnet_2_id = network_layer.require_output("private_subnet_2_id")
public_subnet_1_id = network_layer.require_output("public_subnet_1_id")
public_subnet_2_id = network_layer.require_output("public_subnet_2_id")


# # un-stringify the lists
# private_subnets = json.loads(private_subnets)
# public_subnets = json.loads(public_subnets)


# Create an ECS cluster to run a container-based service.
cluster = aws.ecs.Cluster("dask-ml-workflows")


# IAM Roles/Policies Defined:
dask_ecs_execution_role = aws.iam.Role(
    "dask-ecs-execution-role",
    description="Elastic Container Service Execution Policy for Dask Clusters",
    assume_role_policy=json.dumps(
        {
            "Version": "2008-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ecs-tasks.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole",
                }
            ],
        }
    ),
)

dask_ecs_execution_policy = aws.iam.RolePolicy(
    "dask-ecs-execution-policy",
    role=dask_ecs_execution_role.id,
    policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "ec2:CreateTags",
                        "ec2:DescribeNetworkInterfaces",
                        "ec2:DescribeSubnets",
                        "ec2:DescribeVpcs",
                        "ecs:DescribeTasks",
                        "ecs:ListAccountSettings",
                        "ecs:RegisterTaskDefinition",
                        "ecs:RunTask",
                        "ecs:StopTask",
                        "ecs:ListClusters",
                        "ecs:DescribeClusters",
                        "ecs:ListTaskDefinitions",
                        "ecs:DescribeTaskDefinition",
                        "ecs:DeregisterTaskDefinition",
                        "iam:ListRoleTags",
                        "logs:DescribeLogGroups",
                    ],
                    "Effect": "Allow",
                    "Resource": "*",
                }
            ],
        }
    ),
)


ecs_s3_task_role = aws.iam.Role(
    "s3-ecs-task-role",
    assume_role_policy=json.dumps(
        {
            "Version": "2008-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ecs-tasks.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole",
                }
            ],
        }
    ),
)

ecs_task_rpa = aws.iam.RolePolicyAttachment(
    "ecs-task-policy",
    role=ecs_s3_task_role.name,
    policy_arn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
)


# Create a SecurityGroup that permits HTTP/TCP: ingress from private subnets on required Dask Ports 8787+8786 and All egress.
workflows_dask_sg = aws.ec2.SecurityGroup(
    "workflows-dask-cluster",
    name="workflows-dask-cluster",
    vpc_id=vpc_id,
    description="Dask-CloudProvider Cluster SG",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp", from_port=8786, to_port=8787, cidr_blocks=["0.0.0.0/0"]
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        )
    ],
)

"""An AWS Python Pulumi program"""
# REF: https://github.com/pulumi/examples/blob/master/aws-py-fargate/__main__.py

import json
import pulumi
import pulumi_aws as aws


# get configs defined in our yaml files
config = pulumi.Config()
network_layer_stack = config.require('network-layer-stack')
pulumi_account = config.require('user-account')


# get settings from stack references
env = pulumi.get_stack()
network_layer = pulumi.StackReference(f'{pulumi_account}/network-layer/{env}')



# Read back the project VPC and subnets id's that were set up in the network-layer-{env}, which we will use.
vpc_id = network_layer.require_output('vcp_id')
private_subnets = network_layer.require_output('private_subnet_ids')
public_subnets = network_layer.require_output('public_subnet_ids')
print(private_subnets)
print(dir(private_subnets))
# un-stringify the lists
private_subnets = json.loads(private_subnets)
public_subnets = json.loads(public_subnets)


# Create an ECS cluster to run a container-based service.
cluster = aws.ecs.Cluster('ml-workflows')


# IAM Roles/Policies Defined:
ecs_execution_role = aws.iam.Role(
    'ecs-execution-role',
    description='Elastic Container Service Execution Policy for Dask Clusters',
	assume_role_policy=json.dumps({
		'Version': '2008-10-17',
		'Statement': [{
			'Sid': '',
			'Effect': 'Allow',
			'Principal': {
				'Service': 'ecs-tasks.amazonaws.com'
			},
			'Action': 'sts:AssumeRole',
		}]
	}))

ecs_execution_policy = aws.iam.RolePolicy(
    'ecs-execution-policy',
    role=test_role.id,
    policy=json.dumps({
        'Version': '2012-10-17',
        'Statement': [{
            'Action': [
                'ec2:CreateTags',
                'ec2:DescribeNetworkInterfaces',
                'ec2:DescribeSubnets',
                'ec2:DescribeVpcs',
                'ecs:DescribeTasks',
                'ecs:ListAccountSettings',
                'ecs:RegisterTaskDefinition',
                'ecs:RunTask',
                'ecs:StopTask',
                'ecs:ListClusters',
                'ecs:DescribeClusters',
                'ecs:ListTaskDefinitions',
                'ecs:DescribeTaskDefinition',
                'ecs:DeregisterTaskDefinition',
                'iam:ListRoleTags',
                'logs:DescribeLogGroups'
            ],
            'Effect': 'Allow',
            'Resource': [
                '*'
            ]
        }]
    }))


ecs_task_role = aws.iam.Role(
    'ecs-task-role',
	assume_role_policy=json.dumps({
		'Version': '2008-10-17',
		'Statement': [{
			'Sid': '',
			'Effect': 'Allow',
			'Principal': {
				'Service': 'ecs-tasks.amazonaws.com'
			},
			'Action': 'sts:AssumeRole',
		}]
	}))

ecs_task_rpa = aws.iam.RolePolicyAttachment(
    'ecs-task-policy',
	role=role.name,
	policy_arn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess',
)


# Create a SecurityGroup that permits HTTP/TCP: ingress from private subnets on required Dask Ports 8787+8786 and All egress.
workflows_dask_sg = aws.ec2.SecurityGroup(
    'workflows-dask-cluster',
	vpc_id=vpc_id,
	description='Dask-CloudProvider Cluster SG',
	ingress=[aws.ec2.SecurityGroupIngressArgs(
		protocol='tcp',
		from_port=8786,
		to_port=8787,
		cidr_blocks=['10.0.2.0/24', '10.0.3.0/24'], # restricting it to our public / private subnets here since we don't need '0.0.0.0/0' for any public access like we'd need for an API in Fargate/ECS
	)],
  	egress=[aws.ec2.SecurityGroupEgressArgs(
		protocol='-1',
		from_port=0,
		to_port=0,
		cidr_blocks=['0.0.0.0/0'],
	)],
)
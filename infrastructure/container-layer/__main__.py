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
vpc_azs = network_layer.require_output('vpc_azs')
private_subnets_1 = network_layer.require_output('private_subnet_id_1')
private_subnet_2 = network_layer.require_output('private_subnet_id_2')
public_subnets_1 = network_layer.require_output('public_subnet_id_1')
public_subnets_2 = network_layer.require_output('public_subnet_id_2')

# # un-stringify the lists
# private_subnets = json.loads(private_subnets)
# public_subnets = json.loads(public_subnets)


# Create an ECS cluster to run a container-based service.
cluster = aws.ecs.Cluster('ml-workflows')


# IAM Roles/Policies Defined:
dask_ecs_execution_role = aws.iam.Role(
    'dask-ecs-execution-role',
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

dask_ecs_execution_policy = aws.iam.RolePolicy(
    'dask-ecs-execution-policy',
    role=dask_ecs_execution_role.id,
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


ecs_s3_task_role = aws.iam.Role(
    's3-ecs-task-role',
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
	role=ecs_s3_task_role.name,
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
		cidr_blocks=['0.0.0.0/0']
	)],
  	egress=[aws.ec2.SecurityGroupEgressArgs(
		protocol='-1',
		from_port=0,
		to_port=0,
		cidr_blocks=['0.0.0.0/0'],
	)],
)



# ======================================================================================================================
# Prefect Agent Containers


# Create an IAM role that can be used by our service's task.
agent_ecs_execution_role = aws.iam.Role('agent-task-execution-role',
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
	}),
)

agent_ecs_execution_policy = aws.iam.RolePolicyAttachment('agent-task-execution-policy',
	role=agent_task_exec_role.name,
	policy_arn='arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy',
)

# TODO: add the secrets in here
# Spin up service running our container image for running Prefect Agents
agent_task_definition = aws.ecs.TaskDefinition('app-task',
    family='agent-ecs-task-definition',
    cpu='256',
    memory='512',
    network_mode='awsvpc',
    requires_compatibilities=['FARGATE'],
    execution_role_arn=agent_ecs_execution_role.arn,
    container_definitions=json.dumps([{
		'name': 'prefect-agent',
		'image': 'brontomerus/prefect-agent:aws-github-dask_cp',
		'portMappings': [
			{
				'containerPort': 80,
				'hostPort': 80,
				'protocol': 'tcp'
			}
		],
		'environment': [
			{
				'name': 'EXTRA_PIP_PACKAGES', 
				'value': 'pyarrow s3fs boto3'
			},
			{
				'name': 'PREFECT_AGENT_NAME', 
				'value': 'Dev-Agent'
			},
			{
				'name': 'PREFECT_AGENT', 
				'value': 'local'
			},
			{
				'name': 'PREFECT_BACKEND', 
				'value': 'cloud'
			},
			{
				'name': 'LABELS', 
				'value': '-l dev -l dask'
			},
			{
				'name': 'AWS_DEFAULT_REGION', 
				'value': 'us-east-2'
			},
		],
		'secrets': [
			{
				'name': 'GITHUB_ACCESS_TOKEN',
				'value': ''
			},
			{
				'name': 'PREFECT_CLOUD_TOKEN',
				'value': ''
			}
		]

	)
    placement_constraints=[aws.ecs.TaskDefinitionPlacementConstraintArgs(
        type="memberOf",
        expression=vpc_azs,
    )]
	}])
)

service = aws.ecs.Service('app-svc',
	cluster=cluster.arn,
    desired_count=3,
    launch_type='FARGATE',
    task_definition=task_definition.arn,
    network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
		assign_public_ip=True,
		subnets=default_vpc_subnets.ids,
		security_groups=[group.id],
	),
    load_balancers=[aws.ecs.ServiceLoadBalancerArgs(
		target_group_arn=atg.arn,
		container_name='my-app',
		container_port=80,
	)],
    opts=ResourceOptions(depends_on=[wl]),
)

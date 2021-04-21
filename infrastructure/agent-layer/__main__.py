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



# Read back the project VPC and subnets id"s that were set up in the network-layer-{env}, which we will use.
vpc_id = network_layer.require_output("vcp_id")
vpc_azs = network_layer.require_output("vpc_azs")
private_subnets_1 = network_layer.require_output("private_subnet_id_1")
private_subnet_2 = network_layer.require_output("private_subnet_id_2")
public_subnets_1 = network_layer.require_output("public_subnet_id_1")
public_subnets_2 = network_layer.require_output("public_subnet_id_2")

# # un-stringify the lists
# private_subnets = json.loads(private_subnets)
# public_subnets = json.loads(public_subnets)


# Create an ECS cluster to run a container-based service.
agent_cluster = aws.ecs.Cluster("prefect-agents")



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
agent_task_definition = aws.ecs.TaskDefinition('agent-task-definition',
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
				'containerPort': 8080,
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
	}]
    # ,placement_constraints=[aws.ecs.TaskDefinitionPlacementConstraintArgs(
    #         type="memberOf",
    #         expression=vpc_azs,
    #     )]
)

agents_ecs_service = aws.ecs.Service("agents-ecs-service",
	cluster=agent_cluster.id,
    task_definition=agent_task_definition.arn,
    desired_count=1,
    launch_type="FARGATE",
    iam_role=agent_ecs_execution_role.arn,
    network_configuration=aws.ecs.ServiceNetworkConfigurationArgs( # TODO: set up a load balancer here
		assign_public_ip=True,
		subnets=[private_subnet_id_1, private_subnet_id_2], # does a list
		security_groups=[group.id], # TODO: set up sg groups
	),
    load_balancers=[aws.ecs.ServiceLoadBalancerArgs( # TODO: set up a load balancer here
		target_group_arn=aws_lb_target_group.arn,
		container_name="dev-agent",
		container_port=80,
	)],
    placement_constraints=[aws.ecs.TaskDefinitionPlacementConstraintArgs(
            type="memberOf",
            expression=vpc_azs,
        )]
    opts=pulumi.ResourceOptions(depends_on=[agents_ecs_execution_policy])
)


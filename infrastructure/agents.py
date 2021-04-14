import json
import vpc
import pulumi
import pulumi_aws as aws


# Create an ECS cluster to run a container-based service.
agent_cluster = aws.ecs.Cluster('ml-workflows-agents')


# ======================================================================================================================
# Prefect Agent Containers


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
        expression=vpc.vpc_azs,
    )]
	}])
)

service = aws.ecs.Service('app-svc',
	cluster=agent_cluster.arn,
    desired_count=3,
    launch_type='FARGATE',
    task_definition=agent_task_definition.arn,
    network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
		assign_public_ip=True,
		subnets=[vpc.workflows_private_1.id,vpc.workflows_private_2.id],
		security_groups=[vpc.agent_security_group.id],
	),
    load_balancers=[aws.ecs.ServiceLoadBalancerArgs(
		target_group_arn=atg.arn, #TODO: what is this
		container_name='agent',
		container_port=80,
	)],
    opts=ResourceOptions(depends_on=[wl]),
)

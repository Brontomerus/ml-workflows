"""An AWS Python Pulumi program"""
# REF: https://github.com/pulumi/examples/blob/master/aws-py-fargate/__main__.py

import json
import os
import pulumi
import pulumi_aws as aws

SECRETS = {
    "prefect_cloud_token": os.getenv("PREFECT_CLOUD_TOKEN"),
    "github_access_token": os.getenv("GITHUB_ACCESS_TOKEN"),
}

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
private_subnet_1_id = network_layer.require_output("private_subnet_1_id")
private_subnet_2_id = network_layer.require_output("private_subnet_2_id")
public_subnet_1_id = network_layer.require_output("public_subnet_1_id")
public_subnet_2_id = network_layer.require_output("public_subnet_2_id")


# # un-stringify the lists
# private_subnets = json.loads(private_subnets)
# public_subnets = json.loads(public_subnets)


# Create an ECS cluster to run a container-based service.
agent_cluster = aws.ecs.Cluster("prefect-agents")


agent_secrets = aws.secretsmanager.Secret("agent-secrets",
    description="Prefect Agent secrets for various credentials for operating the hybrid cloud model"
    # TODO: Set up KMS Key
)
agent_secrets_version_1 = aws.secretsmanager.SecretVersion("agent-secrets-version-1",
    secret_id=agent_secrets.id,
    secret_string=json.dumps(SECRETS),
)



# Create a SecurityGroup that permits HTTP ingress and unrestricted egress.
agent_sg = aws.ec2.SecurityGroup('agent-sg',
	vpc_id=vpc_id,
	description='Enable HTTP access',
	ingress=[aws.ec2.SecurityGroupIngressArgs(
		protocol='tcp',
		from_port=80,
		to_port=80,
		cidr_blocks=['0.0.0.0/0'],
	)],
  	egress=[aws.ec2.SecurityGroupEgressArgs(
		protocol='-1',
		from_port=0,
		to_port=0,
		cidr_blocks=['0.0.0.0/0'],
	)],
)

# Create a load balancer to listen for HTTP traffic on port 80.
agent_alb = aws.lb.LoadBalancer('agent-lb',
	security_groups=[agent_sg.id],
	subnets=[private_subnet_1_id, private_subnet_2_id],
)

agent_atg = aws.lb.TargetGroup('agent-tg',
	port=80,
	protocol='HTTP',
	target_type='ip',
	vpc_id=vpc_id,
)

agent_wl = aws.lb.Listener('agent-wl',
	load_balancer_arn=agent_alb.arn,
	port=80,
	default_actions=[aws.lb.ListenerDefaultActionArgs(
		type='forward',
		target_group_arn=agent_atg.arn,
	)],
)





# Create an IAM role that can be used by our service"s task.
agent_ecs_execution_role = aws.iam.Role("agent-task-execution-role",
    assume_role_policy=json.dumps(
        {
            "Version": "2012-10-17",
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


# TODO: don't use * for Resource, especially for ssm/secretsmanager
agent_ecs_execution_policy = aws.iam.RolePolicy("agent-ecs-execution-policy",
    role=agent_ecs_execution_role.id,
    policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Resource": "*",
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "ssm:GetParameters",
                        "secretsmanager:GetSecretValue",
                        "kms:Decrypt"
                    ],
                    "Resource": "*",
                },
            ],
        }
    ),
)

agent_rpa = aws.iam.RolePolicyAttachment('agent-task-exec-policy',
	role=agent_ecs_execution_role.name,
	policy_arn='arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy',
)

# Create a log group to store ECS Logs
agent_log_group = aws.cloudwatch.LogGroup("agent-ecs", 
    name="agent-ecs",
    retention_in_days=30,
    tags={
        "Application": "agent-layer",
        "Environment": "dev",
    }
)


# Spin up service running our container image for running Prefect Agents
# ref for secrets: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data-secrets.html
agent_task_definition = aws.ecs.TaskDefinition("agent-task-definition",
    family="agent-ecs-task-definition",
    cpu="512",
    memory="2048",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=agent_ecs_execution_role.arn,
    container_definitions=pulumi.Output.all(
        secrets = agent_secrets.arn,
        log_group = agent_log_group.name
    ).apply(
            lambda args:
        json.dumps(
            [
                {
                    "name": "prefect-agent",
                    "image": "brontomerus/prefect-agent:aws-github-dask_cp",
                    "portMappings": [
                        {
                            "containerPort": 80,
                            "hostPort": 80,
                            "protocol": "tcp"
                        }
                    ],
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": f"{args['log_group']}",
                            "awslogs-region": "us-east-2",
                            "awslogs-stream-prefix": "agent-ecs-test"
                        }
                    },
                    "environment": [
                        {
                            "name": "EXTRA_PIP_PACKAGES", 
                            "value": "pyarrow s3fs boto3"
                        },
                        {
                            "name": "PREFECT_AGENT_NAME", 
                            "value": "ml-workflows-DEV-Agent"
                        },
                        {
                            "name": "PREFECT_AGENT",
                            "value": "local"
                        },
                        {
                            "name": "PREFECT_BACKEND",
                            "value": "cloud"
                        },
                        {
                            "name": "LABELS",
                            "value": "-l dev -l dask"
                        },
                        {
                            "name": "AWS_DEFAULT_REGION",
                            "value": "us-east-2"
                        },
                        {
                            "name": "PREFECT_CLOUD_TOKEN",
                            "value": os.getenv("PREFECT_CLOUD_TOKEN")
                        }
                    ],
                    "secrets": [
                        {
                            "name": "GITHUB_ACCESS_TOKEN",
                            "valueFrom": f"{args['secrets']}:github_access_token::",
                        },
                        {
                            "name": "PREFECT_CLOUD_TOKEN",
                            "valueFrom": f"{args['secrets']}:prefect_cloud_token::",
                        }               
                    ],
                }
            ]
        )
    )
)


agents_ecs_service = aws.ecs.Service("agents-ecs-service",
    cluster=agent_cluster.id,
    task_definition=agent_task_definition.arn,
    desired_count=1,
    launch_type="FARGATE",
    # iam_role=agent_ecs_execution_role.arn,
    network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
        assign_public_ip=False,
        subnets=[private_subnet_1_id, private_subnet_2_id],
        security_groups=[agent_sg.id]
    ),
    # TODO: set up a load balancer here maybe?
    load_balancers=[aws.ecs.ServiceLoadBalancerArgs(
		target_group_arn=agent_atg.arn,
		container_name='prefect-agent',
		container_port=80,
	)],
    opts=pulumi.ResourceOptions(depends_on=[agent_wl]),
)

import json
import pulumi
import pulumi_aws as aws


# =======================================================================
# Dask IAM's
# =======================================================================

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

# =======================================================================
# Agent IAM's
# =======================================================================

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
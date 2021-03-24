'''An AWS Python Pulumi program'''
# REF: https://github.com/pulumi/examples/blob/master/aws-py-fargate/__main__.py

import pulumi
import json
from pulumi_aws import aws




config = pulumi.Config()

network_layer_stack = config.require('network-layer-stack')



# Create an AWS resource (S3 Bucket)
bucket = aws.s3.Bucket('load-balancer-bucket-')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)


# Read back the project VPC and subnets id's that were set up in the network-layer-{env}, which we will use.
vpc_id = network_layer_stack.require_output('vcp_id')
private_subnets = network_layer_stack.require_output('private_subnet_ids'))
public_subnets = network_layer_stack.require_output('public_subnet_ids'))

# un-stringify the lists
private_subnets = json.loads(private_subnets)
public_subnets = json.loads(public_subnets)


# TODO: need to add in the security groups for the internal ALB and all that jazz


internal_alb = aws.lb.LoadBalancer(
	'workflows-private-alb',
	internal=True,
    load_balancer_type='application',
    subnet_mappings=[
        aws.lb.LoadBalancerSubnetMappingArgs(
            subnet_id=private_subnet_ids[0],
            private_ipv4_address='10.0.2.3',
        ),
        aws.lb.LoadBalancerSubnetMappingArgs(
            subnet_id=private_subnet_ids[1],
            private_ipv4_address='10.0.3.3',
        ),
    ]
	subnets=private_subnet_ids,
	# security_groups=,
	tags={'Name': 'workflows'})


dummy_target_group = aws.lb.TargetGroup(
	'workflows-alb-dummy-target-group',
	port=80,
	protocol='HTTP',
	target_type='ip',
	vpc_id=vpc_id,
)

alb_listener = aws.lb.Listener(
	'workflows-alb-listener',
	load_balancer_arn=internal_alb.arn,
	port=80,
	default_actions=[
		aws.lb.ListenerDefaultActionArgs(
			type='forward',
			target_group_arn=dummy_target_group.arn,
		)],
	)




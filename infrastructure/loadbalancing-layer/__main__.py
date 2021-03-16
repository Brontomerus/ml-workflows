"""An AWS Python Pulumi program"""
# REF: https://github.com/pulumi/examples/blob/master/aws-py-fargate/__main__.py

import pulumi
import json
from pulumi_aws import s3




config = pulumi.Config()

network_layer_stack = config.require('network-layer-stack')



# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('load-balancer-bucket-')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)


# Read back the default VPC and public subnets, which we will use.
vpc = network_layer_stack.require_output("vcp_id")

vpc_subnets = aws.ec2.get_subnet_ids(vpc_id=network_layer_stack.require_output("vcp_id"))

# Create a SecurityGroup that permits HTTP ingress and unrestricted egress.
group = aws.ec2.SecurityGroup('web-secgrp',
	vpc_id=vpc.id,
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
alb = aws.lb.LoadBalancer('app-lb',
	security_groups=[group.id],
	subnets=vpc_subnets.ids,
)

atg = aws.lb.TargetGroup('app-tg',
	port=80,
	protocol='HTTP',
	target_type='ip',
	vpc_id=vpc.id,
)

wl = aws.lb.Listener('web',
	load_balancer_arn=alb.arn,
	port=80,
	default_actions=[aws.lb.ListenerDefaultActionArgs(
		type='forward',
		target_group_arn=atg.arn,
	)],
)


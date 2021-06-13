'''An AWS Python Pulumi program'''
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



# TODO: need to add in the security groups for the internal ALB and all that jazz




internal_alb = aws.lb.LoadBalancer(
	'workflows-private-alb',
	internal=True,
    load_balancer_type='application',
    subnet_mappings=[
        aws.lb.LoadBalancerSubnetMappingArgs(
            subnet_id=private_subnet_ids[0],
            private_ipv4_address='10.0.2.5',
        ),
        aws.lb.LoadBalancerSubnetMappingArgs(
            subnet_id=private_subnet_ids[1],
            private_ipv4_address='10.0.3.5',
        ),
    ]
	subnets=private_subnet_ids,
	# security_groups=,
	tags={'Name': 'workflows'}
)


dummy_target_group = aws.lb.TargetGroup(
	'workflows-alb-dummy-target-group',
	port=80,
	protocol='HTTP',
	target_type='ip',
	vpc_id=vpc_id,
	tags={'Name': 'workflows'}
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
	tags={'Name': 'workflows'}
)





# export for downstream layers
pulumi.export("vcp_id", workflows.id)
pulumi.export("public_subnet_1_id", workflows_public_1.id)
pulumi.export("public_subnet_2_id", workflows_public_2.id)

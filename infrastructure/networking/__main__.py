"""A Python Pulumi program"""
# REF: https://github.com/pulumi/examples/tree/master/aws-stackreference-architecture/networking
# REF: https://github.com/pulumi/examples/blob/master/aws-py-resources/__main__.py



import pulumi
import pulumi_aws as aws


# Create an AWS resource (S3 Bucket)
bucket = aws.s3.Bucket('networking-bucket')

# Export the name of the bucket
pulumi.export('networking-bucket-',  bucket.id)

subnets = {
    "workflows-public-1": "10.0.0.0/24",
    "workflows-public-2": "10.0.1.0/24",
    "workflows-private-1": "10.0.2.0/24",
    "workflows-private-2": "10.0.3.0/24"
}


workflows = aws.ec2.Vpc("workflows", cidr_block="10.0.0.0/16")

az = aws.get_availability_zones(state="available")


workflows_public_1 = aws.ec2.Subnet(
    "workflows-public-1",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-public-1"],
    availability_zone=az.names[0],
    map_public_ip_on_launch=True,
    tags={
        "Name": "workflows",
    }
)

workflows_public_2 = aws.ec2.Subnet(
    "workflows-public-2",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-public-2"],
    availability_zone=az.names[1],
    map_public_ip_on_launch=True,
    tags={
        "Name": "workflows",
    }
)

workflows_private_1 = aws.ec2.Subnet(
    "workflows-private-1",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-private-1"],
    availability_zone=az.names[0],
    tags={
        "Name": "workflows",
    }
)

workflows_private_2 = aws.ec2.Subnet(
    "workflows-private-2",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-private-2"],
    availability_zone=az.names[1],
    tags={
        "Name": "workflows",
    }
)


internet_gateway = aws.ec2.InternetGateway(
    "workflows-internet_gateway",
    vpc_id=workflows.id,
    tags={
        "Name": "workflows",
    }
)

routetable_public = aws.ec2.RouteTable(
    resource_name='workflows-public-routetable',
    vpc_id=workflows.id,
    routes=[{
            "cidrBlock": "0.0.0.0/0",
            "gatewayId": internet_gateway.id
    }]
)

routetable_public_1_association = aws.ec2.RouteTableAssociation(
    resource_name='workflows-public-1-rt-assoc',
    subnet_id=workflows_public_1.id,
    route_table_id=routetable_public
)

routetable_public_2_association = aws.ec2.RouteTableAssociation(
    resource_name='workflows-public-2-rt-assoc',
    subnet_id=workflows_public_2.id,
    route_table_id=routetable_public
)


# allow_tls_public_group = aws.ec2.SecurityGroup("allowTls",
#     description="Allow TLS inbound traffic",
#     vpc_id=aws_vpc["main"]["id"],
#     ingress=[aws.ec2.SecurityGroupIngressArgs(
#         description="TLS from VPC",
#         from_port=443,
#         to_port=443,
#         protocol="tcp",
#         cidr_blocks=[aws_vpc["main"]["cidr_block"]],
#     )],
#     egress=[aws.ec2.SecurityGroupEgressArgs(
#         from_port=0,
#         to_port=0,
#         protocol="-1",
#         cidr_blocks=["0.0.0.0/0"],
#     )],
#     tags={
#         "Name": "allow_tls",
#     }
# )

# ssh_public_group = aws.ec2.SecurityGroup('workflows-ssh-public-agents',
#     description='Enable HTTP access',
#     ingress=[aws.ec2.SecurityGroupIngressArgs(
#         protocol='SSH',
#         from_port=22,
#         to_port=22,
#         cidr_blocks=['0.0.0.0/0'],
#     )])














workflows_gateway_eib = aws.ec2.Eip(
    "workflows-gateway-eib",
    vpc=True
)


nat_gateway = aws.ec2.NatGateway(
    "workflows-private-1-nat-gateway",
    allocation_id=workflows_gateway_eib.id,
    subnet_id=workflows_private_1.id
)


routetable_private_1 = aws.ec2.RouteTable(
    resource_name='workflows-private-1-routetable',
    vpc_id=workflows.id,
    routes=[{
            "cidrBlock": "0.0.0.0/0",
            "gatewayId": nat_gateway.id
    }]
)

routetable_private_1_association = aws.ec2.RouteTableAssociation(
    resource_name='workflows route table association',
    subnet_id=workflows_private_1.id,
    route_table_id=routetable_private_1
)















# # Create an IAM role that can be used by our service's task.
# role = aws.iam.Role('task-exec-role',
# 	assume_role_policy=json.dumps({
# 		'Version': '2008-10-17',
# 		'Statement': [{
# 			'Sid': '',
# 			'Effect': 'Allow',
# 			'Principal': {
# 				'Service': 'ecs-tasks.amazonaws.com'
# 			},
# 			'Action': 'sts:AssumeRole',
# 		}]
# 	}),
# )

# rpa = aws.iam.RolePolicyAttachment('task-exec-policy',
# 	role=role.name,
# 	policy_arn='arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy',
# )
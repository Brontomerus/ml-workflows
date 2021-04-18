# https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html
import pulumi
import pulumi_aws as aws


config = pulumi.Config()
stack = config.require('environment')


# Create edge AWS resource(s) (S3 Buckets)
bucket = aws.s3.Bucket('networking-bucket-')
output_bucket = aws.s3.Bucket('output-bucket-')
model_ops_bucket = aws.s3.Bucket('model-ops-bucket-')



subnets = {
    "workflows-public-1": "10.0.0.0/24",
    "workflows-public-2": "10.0.1.0/24",
    "workflows-private-1": "10.0.2.0/24",
    "workflows-private-2": "10.0.3.0/24"
}

workflows = aws.ec2.Vpc(
    "workflows",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    cidr_block="10.0.0.0/16",
    tags={"Name": "workflows"})

az = aws.get_availability_zones(state="available")

workflows_public_1 = aws.ec2.Subnet(
    "workflows-public-1",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-public-1"],
    availability_zone=az.names[0],
    map_public_ip_on_launch=True,
    tags={"Name": "workflows"})

workflows_public_2 = aws.ec2.Subnet(
    "workflows-public-2",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-public-2"],
    availability_zone=az.names[1],
    map_public_ip_on_launch=True,
    tags={"Name": "workflows"})

workflows_private_1 = aws.ec2.Subnet(
    "workflows-private-1",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-private-1"],
    availability_zone=az.names[0],
    map_public_ip_on_launch=False,
    tags={"Name": "workflows"})

workflows_private_2 = aws.ec2.Subnet(
    "workflows-private-2",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-private-2"],
    availability_zone=az.names[1],
    map_public_ip_on_launch=False,
    tags={"Name": "workflows"})


internet_gateway = aws.ec2.InternetGateway(
    "workflows-internet_gateway",
    vpc_id=workflows.id,
    tags={"Name": "workflows"})

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
    route_table_id=routetable_public)

routetable_public_2_association = aws.ec2.RouteTableAssociation(
    resource_name='workflows-public-2-rt-assoc',
    subnet_id=workflows_public_2.id,
    route_table_id=routetable_public)







workflows_gateway_eip_1 = aws.ec2.Eip(
    "workflows-gateway-eip-1",
    vpc=True)
workflows_gateway_eip_2 = aws.ec2.Eip(
    "workflows-gateway-eip-2",
    vpc=True)




nat_gateway_1 = aws.ec2.NatGateway(
    "workflows-private-1-nat-gateway",
    allocation_id=workflows_gateway_eip_1.id,
    subnet_id=workflows_public_1.id)
nat_gateway_2 = aws.ec2.NatGateway(
    "workflows-private-2-nat-gateway",
    allocation_id=workflows_gateway_eip_2.id,
    subnet_id=workflows_public_2.id)


routetable_private_1 = aws.ec2.RouteTable(
    'workflows-private-1-routetable',
    vpc_id=workflows.id,
    routes=[{
        "cidrBlock": "0.0.0.0/0",
        "gatewayId": nat_gateway_1.id
        }]
    )
routetable_private_1_association = aws.ec2.RouteTableAssociation(
    'workflows-private-1-rt-assoc',
    subnet_id=workflows_private_1.id,
    route_table_id=routetable_private_1)


routetable_private_2 = aws.ec2.RouteTable(
    'workflows-private-2-routetable',
    vpc_id=workflows.id,
    routes=[{
        "cidrBlock": "0.0.0.0/0",
        "gatewayId": nat_gateway_2.id
        }]
    )
routetable_private_2_association = aws.ec2.RouteTableAssociation(
    'workflows-private-2-rt-assoc',
    subnet_id=workflows_private_2.id,
    route_table_id=routetable_private_2)



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

# Create a SecurityGroup that permits HTTP/TCP: ingress from private subnets on required Dask Ports 8787+8786 and All egress.
agent_security_group = aws.ec2.SecurityGroup( #TODO: will this work? prob not...
    'workflows-agent-cluster',
	vpc_id=vpc_id,
	description='Prefect Agent Security Group',
  	egress=[aws.ec2.SecurityGroupEgressArgs(
		protocol='-1',
		from_port=0,
		to_port=0,
		cidr_blocks=['0.0.0.0/0'],
	)],
)



# TODO: Do we still need this? probably not
# export for downstream uses
pulumi.export("vcp_id", workflows.id)
pulumi.export('public_subnet_1_id', workflows_public_1.id)
pulumi.export('public_subnet_2_id', workflows_public_2.id)
pulumi.export('private_subnet_1_id', workflows_private_1.id)
pulumi.export('private_subnet_2_id', workflows_private_2.id)
pulumi.export('subnets', subnets)

pulumi.export("vpc_azs", [az.names[0], az.names[1]])

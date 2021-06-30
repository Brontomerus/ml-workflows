"""A Python Pulumi program"""
# REF: https://github.com/pulumi/examples/tree/master/aws-stackreference-architecture/networking
# REF: https://github.com/pulumi/examples/blob/master/aws-py-resources/__main__.py

import pulumi
import pulumi_aws as aws


config = pulumi.Config()
stack = config.require("environment")


# Create edge AWS resource(s) (S3 Buckets)
bucket = aws.s3.Bucket("networking-bucket-")
output_bucket = aws.s3.Bucket("output-bucket-")
model_ops_bucket = aws.s3.Bucket("model-ops-bucket-")

# Export the name of the buckets
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_name", output_bucket.id)
pulumi.export("bucket_name", model_ops_bucket.id)


# =====================================================================================
# VPC & Subnets
# =====================================================================================


subnets = {
    "workflows-public-1": "10.0.0.0/24",
    "workflows-public-2": "10.0.1.0/24",
    "workflows-private-1": "10.0.2.0/24",
    "workflows-private-2": "10.0.3.0/24",
}

workflows = aws.ec2.Vpc(
    "workflows",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    cidr_block="10.0.0.0/16",
    tags={"Name": "workflows"},
)

az = aws.get_availability_zones(state="available")

workflows_public_1 = aws.ec2.Subnet(
    "workflows-public-1",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-public-1"],
    availability_zone=az.names[0],
    map_public_ip_on_launch=True,
    tags={"Name": "workflows"},
)

workflows_public_2 = aws.ec2.Subnet(
    "workflows-public-2",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-public-2"],
    availability_zone=az.names[1],
    map_public_ip_on_launch=True,
    tags={"Name": "workflows"},
)

workflows_private_1 = aws.ec2.Subnet(
    "workflows-private-1",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-private-1"],
    availability_zone=az.names[0],
    map_public_ip_on_launch=False,
    tags={"Name": "workflows"},
)

workflows_private_2 = aws.ec2.Subnet(
    "workflows-private-2",
    vpc_id=workflows.id,
    cidr_block=subnets["workflows-private-2"],
    availability_zone=az.names[1],
    map_public_ip_on_launch=False,
    tags={"Name": "workflows"},
)


internet_gateway = aws.ec2.InternetGateway(
    "workflows-internet_gateway", vpc_id=workflows.id, tags={"Name": "workflows"}
)

routetable_public = aws.ec2.RouteTable(
    resource_name="workflows-public-routetable",
    vpc_id=workflows.id,
    routes=[{"cidrBlock": "0.0.0.0/0", "gatewayId": internet_gateway.id}],
)

routetable_public_1_association = aws.ec2.RouteTableAssociation(
    resource_name="workflows-public-1-rt-assoc",
    subnet_id=workflows_public_1.id,
    route_table_id=routetable_public,
)

routetable_public_2_association = aws.ec2.RouteTableAssociation(
    resource_name="workflows-public-2-rt-assoc",
    subnet_id=workflows_public_2.id,
    route_table_id=routetable_public,
)


# =====================================================================================
# Route Tables & Internet Connectivity
# =====================================================================================


workflows_gateway_eip_1 = aws.ec2.Eip("workflows-gateway-eip-1", vpc=True)
workflows_gateway_eip_2 = aws.ec2.Eip("workflows-gateway-eip-2", vpc=True)


nat_gateway_1 = aws.ec2.NatGateway(
    "workflows-private-1-nat-gateway",
    allocation_id=workflows_gateway_eip_1.id,
    subnet_id=workflows_public_1.id,
)
nat_gateway_2 = aws.ec2.NatGateway(
    "workflows-private-2-nat-gateway",
    allocation_id=workflows_gateway_eip_2.id,
    subnet_id=workflows_public_2.id,
)


routetable_private_1 = aws.ec2.RouteTable(
    "workflows-private-1-routetable",
    vpc_id=workflows.id,
    routes=[{"cidrBlock": "0.0.0.0/0", "gatewayId": nat_gateway_1.id}],
)
routetable_private_1_association = aws.ec2.RouteTableAssociation(
    "workflows-private-1-rt-assoc",
    subnet_id=workflows_private_1.id,
    route_table_id=routetable_private_1,
)


routetable_private_2 = aws.ec2.RouteTable(
    "workflows-private-2-routetable",
    vpc_id=workflows.id,
    routes=[{"cidrBlock": "0.0.0.0/0", "gatewayId": nat_gateway_2.id}],
)
routetable_private_2_association = aws.ec2.RouteTableAssociation(
    "workflows-private-2-rt-assoc",
    subnet_id=workflows_private_2.id,
    route_table_id=routetable_private_2,
)



# Create a SecurityGroup that permits ingress to public
agent_security_group = aws.ec2.SecurityGroup("public-sg",
    name="public-sg",
    vpc_id=workflows.id,
    description="Enable Access to Public Subnets",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            description="All Ingress Enabled",
            protocol=-1,
            from_port=0,
            to_port=0,
            cidr_blocks=['0.0.0.0/0'],
        )
	],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            description="Egress from Agent ECS Containers to Anywhere",
            protocol="tcp",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        )
    ],
)



# =====================================================================================
# Finish Up
# =====================================================================================


# export for downstream layers
pulumi.export("vcp_id", workflows.id)
pulumi.export("public_subnet_1_id", workflows_public_1.id)
pulumi.export("public_subnet_2_id", workflows_public_2.id)
pulumi.export("private_subnet_1_id", workflows_private_1.id)
pulumi.export("private_subnet_2_id", workflows_private_2.id)
pulumi.export("private_subnet_1_CIDR", workflows_private_1.cidr_block)
pulumi.export("subnets", subnets)

pulumi.export("vpc_azs", [az.names[0], az.names[1]])

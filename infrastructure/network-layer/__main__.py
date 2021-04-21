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
pulumi.export("bucket_name",  bucket.id)
pulumi.export("bucket_name",  output_bucket.id)
pulumi.export("bucket_name",  model_ops_bucket.id)



# =====================================================================================
# VPC & Subnets
# =====================================================================================



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
    resource_name="workflows-public-routetable",
    vpc_id=workflows.id,
    routes=[{
        "cidrBlock": "0.0.0.0/0",
        "gatewayId": internet_gateway.id
        }]
    )

routetable_public_1_association = aws.ec2.RouteTableAssociation(
    resource_name="workflows-public-1-rt-assoc",
    subnet_id=workflows_public_1.id,
    route_table_id=routetable_public)

routetable_public_2_association = aws.ec2.RouteTableAssociation(
    resource_name="workflows-public-2-rt-assoc",
    subnet_id=workflows_public_2.id,
    route_table_id=routetable_public)





# =====================================================================================
# Route Tables & Internet Connectivity
# =====================================================================================


workflows_gateway_eip_1 = aws.ec2.Eip(
    "workflows-gateway-eip-1",
    vpc=True)
workflows_gateway_eip_2 = aws.ec2.Eip(
    "workflows-gateway-eip-2",
    vpc=True)




nat_gateway_1 = aws.ec2.NatGateway("workflows-private-1-nat-gateway",
    allocation_id=workflows_gateway_eip_1.id,
    subnet_id=workflows_public_1.id)
nat_gateway_2 = aws.ec2.NatGateway("workflows-private-2-nat-gateway",
    allocation_id=workflows_gateway_eip_2.id,
    subnet_id=workflows_public_2.id)


routetable_private_1 = aws.ec2.RouteTable("workflows-private-1-routetable",
    vpc_id=workflows.id,
    routes=[{
        "cidrBlock": "0.0.0.0/0",
        "gatewayId": nat_gateway_1.id
        }]
    )
routetable_private_1_association = aws.ec2.RouteTableAssociation("workflows-private-1-rt-assoc",
    subnet_id=workflows_private_1.id,
    route_table_id=routetable_private_1)


routetable_private_2 = aws.ec2.RouteTable("workflows-private-2-routetable",
    vpc_id=workflows.id,
    routes=[{
        "cidrBlock": "0.0.0.0/0",
        "gatewayId": nat_gateway_2.id
        }]
    )
routetable_private_2_association = aws.ec2.RouteTableAssociation("workflows-private-2-rt-assoc",
    subnet_id=workflows_private_2.id,
    route_table_id=routetable_private_2)




# =====================================================================================
# VPN
# =====================================================================================





vpn_endpoint = aws.ec2clientvpn.Endpoint("workflows-vpn-endpoint",
    description="workflows-clientvpn",
    server_certificate_arn=aws_acm_certificate["cert"]["arn"],
    client_cidr_block="10.0.0.0/16",
    authentication_options=[aws.ec2clientvpn.EndpointAuthenticationOptionArgs(
        type="certificate-authentication",
        root_certificate_chain_arn=aws_acm_certificate["root_cert"]["arn"],
    )],
    connection_log_options=aws.ec2clientvpn.EndpointConnectionLogOptionsArgs(
        enabled=True,
        cloudwatch_log_group=aws_cloudwatch_log_group["lg"]["name"],
        cloudwatch_log_stream=aws_cloudwatch_log_stream["ls"]["name"],
    ))

vpn_network_association = aws.ec2clientvpn.NetworkAssociation("workflows-vpn-network-assoc",
    description="workflows-vpn-network-assoc"
    client_vpn_endpoint_id=vpn_endpoint.id,
    subnet_id=workflows_private_1.id,
    # security_groups=[
    #     aws_security_group["example1"]["id"],
    #     aws_security_group["example2"]["id"],
    # ]
    )

vpn_route = aws.ec2clientvpn.Route("workflows-vpn-route",
    description="workflows-vpn-route"
    client_vpn_endpoint_id=vpn_endpoint.id,
    destination_cidr_block="0.0.0.0/0",
    target_vpc_subnet_id=vpn_network_association.subnet_id)

vpn_auth_rules = aws.ec2clientvpn.AuthorizationRule("workflows-vpn-auth-rules",
    description="workflows-vpn-auth-rules"
    client_vpn_endpoint_id=vpn_endpoint.id,
    target_network_cidr=workflows_private_1.cidr_block,
    authorize_all_groups=True)










# =====================================================================================
# Finish Up
# =====================================================================================




# export for downstream layers
pulumi.export("vcp_id", workflows.id)
pulumi.export("public_subnet_1_id", workflows_public_1.id)
pulumi.export("public_subnet_2_id", workflows_public_2.id)
pulumi.export("private_subnet_1_id", workflows_private_1.id)
pulumi.export("private_subnet_2_id", workflows_private_2.id)
pulumi.export("subnets", subnets)

pulumi.export("vpc_azs", [az.names[0], az.names[1]])
"""An AWS Python Pulumi program"""

import json
import os
import pulumi
import pulumi_aws as aws


# get configs defined in our yaml files
config = pulumi.Config()
network_layer_stack = config.require("network-layer-stack")
pulumi_account = config.require("user-account")


# get settings from stack references
env = pulumi.get_stack()
network_layer = pulumi.StackReference(f"{pulumi_account}/network-layer/{env}")


# Read back the project VPC and subnets id's that were set up in the network-layer-{env}, which we will use.
vpc_id = network_layer.require_output("vcp_id")
vpc_azs = network_layer.require_output("vpc_azs")
private_subnet_1_id = network_layer.require_output("private_subnet_1_id")
private_subnet_2_id = network_layer.require_output("private_subnet_2_id")
public_subnet_1_id = network_layer.require_output("public_subnet_1_id")
public_subnet_2_id = network_layer.require_output("public_subnet_2_id")
private_subnet_1_CIDR = network_layer.require_output("private_subnet_1_CIDR")

# # un-stringify the lists
# private_subnets = json.loads(private_subnets)
# public_subnets = json.loads(public_subnets)


# Create an AWS resource (S3 Bucket)
bucket = aws.s3.Bucket("my-bucket")

# Export the name of the bucket
pulumi.export("bucket_name", bucket.id)

# need to read these in. created using these instructions: https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/client-authentication.html#mutual
# another helpful video: https://www.youtube.com/watch?v=St8y0xZSn3c
with open("../../../keys/server.key", "rb") as f:
    private_key = f.read().decode("ascii")  # .replace('\n','')

with open("../../../keys/server.crt", "rb") as f:
    crt_body = f.read().decode("ascii")  # .replace('\n','')

with open("../../../keys/ca.crt", "rb") as f:
    ca_chain = f.read().decode("ascii")  # .replace('\n','')


acm_certificate = aws.acm.Certificate(
    "workflows-acm-cert",
    private_key=private_key,
    certificate_body=crt_body,
    certificate_chain=ca_chain,
)


# CloudWatch Logs set up:
vpn_log_group = aws.cloudwatch.LogGroup("workflows-vpn-log-group")
vpn_log_stream = aws.cloudwatch.LogStream(
    "workflows-vpn-log-stream", log_group_name=vpn_log_group.name
)

vpn_endpoint = aws.ec2clientvpn.Endpoint(
    "workflows-vpn-endpoint",
    description="workflows-clientvpn",
    server_certificate_arn=acm_certificate.arn,
    client_cidr_block="10.5.0.0/20",
    authentication_options=[
        aws.ec2clientvpn.EndpointAuthenticationOptionArgs(
            type="certificate-authentication",
            root_certificate_chain_arn=acm_certificate.arn,
        )
    ],
    connection_log_options=aws.ec2clientvpn.EndpointConnectionLogOptionsArgs(
        enabled=True,
        cloudwatch_log_group=vpn_log_group.name,
        cloudwatch_log_stream=vpn_log_stream.name,
    ),
)

vpn_network_association = aws.ec2clientvpn.NetworkAssociation(
    "workflows-vpn-network-assoc",
    client_vpn_endpoint_id=vpn_endpoint.id,
    subnet_id=private_subnet_1_id,
    # security_groups=[
    #     aws_security_group["example1"]["id"],
    #     aws_security_group["example2"]["id"],
    # ]
)

vpn_route = aws.ec2clientvpn.Route(
    "workflows-vpn-route",
    description="workflows-vpn-route",
    client_vpn_endpoint_id=vpn_endpoint.id,
    destination_cidr_block="0.0.0.0/0",
    target_vpc_subnet_id=vpn_network_association.subnet_id,
)

vpn_auth_rules = aws.ec2clientvpn.AuthorizationRule(
    "workflows-vpn-auth-rules",
    description="workflows-vpn-auth-rules",
    client_vpn_endpoint_id=vpn_endpoint.id,
    target_network_cidr=private_subnet_1_CIDR,
    authorize_all_groups=True,
)

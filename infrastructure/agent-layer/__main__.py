"""An AWS Python Pulumi program"""
# REF: https://github.com/pulumi/examples/blob/master/aws-py-webserver/__main__.py
# REF: https://github.com/pulumi/examples/blob/master/aws-py-ec2-provisioners/__main__.py


import pulumi
from pulumi_aws import s3, aws


# Get the config ready to go.
config = pulumi.Config()


# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)


# create the first small bastion SSH server sitting in the public subnet
# ==================================================================================================
bastion_ami = aws.get_ami(
    most_recent="true",
    owners=["137112412989"],
    filters=[{"name":"name","values":["amzn-ami-hvm-*"]}])

workflows_ssh_sg = aws.ec2.SecurityGroup('workflows-ssh',
    description='Enable HTTP access',
    ingress=[
        { 'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0'] }
    ])

bastion_server = aws.ec2.Instance(
    "workflows-bastion",
    instance_type="t2.micro",
    vpc_security_group_ids=[workflows_ssh_sg.id], # reference security group from above
    ami=bastion_ami.id)

pulumi.export('publicIp', bastion_server.public_ip)

# ==================================================================================================




# create the agent host that sits within our private subnet
# ==================================================================================================

workflows_agent_host_sg = aws.ec2.SecurityGroup('workflows-agent-host-ssh',
    description="Enable SSH access",
    ingress=[
        { 'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0'] }
    ])

agent_host_server = aws.ec2.Instance(
    "workflows-agent-host",
    instance_type="t3.large",
    vpc_security_group_ids=[workflows_agent_host_sg.id], # reference security group from above
    ami="ami-0296ac00c5f58aed3") # using a community AMI for Centos7 + docker

pulumi.export('privateIp', agent_host_server.public_ip)

# ==================================================================================================








# create one server in the public subnet
 

# create one server in the private subnet, which can be reached via the public server for maintenance



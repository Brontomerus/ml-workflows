"""An AWS Python Pulumi program"""
# REF: https://github.com/pulumi/examples/blob/master/aws-py-webserver/__main__.py
# REF: https://github.com/pulumi/examples/blob/master/aws-py-ec2-provisioners/__main__.py


import pulumi
from pulumi_aws import s3


# Get the config ready to go.
config = pulumi.Config()


# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)



# If keyName is provided, an existing KeyPair is used, else if publicKey is provided a new KeyPair
# derived from the publicKey is created.
key_name = config.get('keyName')
public_key = config.get('publicKey')

# The privateKey associated with the selected key must be provided (either directly or base64 encoded),
# along with an optional passphrase if needed.
def decode_key(key):
    if key.startswith('-----BEGIN RSA PRIVATE KEY-----'):
        return key
    return key.encode('ascii')
private_key = config.require_secret('privateKey').apply(decode_key)
private_key_passphrase = config.get_secret('privateKeyPassphrase')


size = 't2.micro'
ami = aws.get_ami(most_recent="true",
                  owners=["137112412989"],
                  filters=[{"name":"name","values":["amzn-ami-hvm-*"]}])

group = aws.ec2.SecurityGroup('webserver-secgrp',
    description='Enable HTTP access',
    ingress=[
        { 'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0'] }
    ])

server = aws.ec2.Instance('webserver-www',
    instance_type=size,
    vpc_security_group_ids=[group.id], # reference security group from above
    ami=ami.id)

pulumi.export('publicIp', server.public_ip)
pulumi.export('publicHostName', server.public_dns)






# create one server in the public subnet
 

# create one server in the private subnet, which can be reached via the public server for maintenance



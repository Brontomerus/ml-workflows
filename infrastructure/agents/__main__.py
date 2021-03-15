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

# Create a new security group that permits SSH and web access.
secgrp = aws.ec2.SecurityGroup('secgrp',
    description='Foo',
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(protocol='SSH', from_port=22, to_port=22, cidr_blocks=['0.0.0.0/0'])
    ],
)



# create one server in the public subnet
 

# create one server in the private subnet, which can be reached via the public server for maintenance



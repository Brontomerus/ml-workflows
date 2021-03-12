"""A Python Pulumi program"""

import pulumi
from pulumi_aws import s3
from pulumi_docker import docker 


# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name',  bucket.id)
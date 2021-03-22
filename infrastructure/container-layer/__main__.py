"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('container-bucket-')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)



# Create an ECS cluster to run a container-based service.
cluster = aws.ecs.Cluster('cluster')

# IAM Roles/Policies Defined:
# ...
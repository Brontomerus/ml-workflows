import json
import pulumi
import pulumi_aws as aws

# Create an ECS cluster to run a container-based service.
dask_cluster = aws.ecs.Cluster('ml-workflows')


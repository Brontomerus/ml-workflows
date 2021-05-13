from dotenv import load_dotenv
import dask.dataframe as dd
import pandas as pd
import boto3
import os

from dask_cloudprovider.aws import FargateCluster
from dask.distributed import Client

load_dotenv()

# define our model developement cluster
cluster = FargateCluster(
    n_workers = 4,
    fargate_use_private_ip = False, # I don't really feel like going through the trouble of making this private
    worker_cpu = 1024,
    worker_mem = 4096,
    cluster_arn = os.getenv('AWS_ECS_CLUSTER_ARN'),
    vpc = os.getenv('AWS_VPC_ID'),
    subnets = [os.getenv('AWS_PUBLIC_SUBNET_1')], # use the public subnets from creating them in the IaC
    security_groups = [os.getenv('AWS_DASK_SECURITY_GROUP')],
    scheduler_timeout = '8 minutes', # a bit longer because we're just in "dev" right now
    image = 'daskdev/dask:2021.4.1', 
    # environment = {
    #     'EXTRA_CONDA_PACKAGES': '',
    #     'EXTRA_PIP_PACKAGES': ''
    # }
)
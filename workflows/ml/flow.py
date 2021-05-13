import dask.dataframe as dd
import pandas as pd
import prefect

from dask_ml.xgboost import XGBRegressor

from dask_cloudprovider.aws import FargateCluster
from prefect.client import Secret
from prefect.executors import DaskExecutor
from prefect.run_configs import UniversalRun, LocalRun
from prefect.storage.github import GitHub



class IO:

    @staticmethod
    @task
    def read_data(bucket_name: str, folder_name: str, table_name: str) -> dd.DataFrame:
        data = dd.read_parquet(f"s3://{bucket_name}/{folder_name}/{table_name}/part.*.parquet",engine="pyarrow") # columns=[]
        return data

    @staticmethod
    @task
    def write_to_S3(data: dd.DataFrame, bucket_name: str, folder_name: str, table_name: str) -> None:
        data.to_parquet(path=f"s3://{bucket_name}/{folder_name}/{table_name}", compression="gzip", engine="pyarrow", overwrite=True) 


class ML:

    @staticmethod
    @task
    def feature_engineering(data: dd.DataFrame) -> dd.DataFrame:
        # data = data.repartition(npartitions=1)
        data = data.persist()

    @staticmethod
    @task
    def inference(data: dd.DataFrame) -> dd.DataFrame:
        pass




# prefect.context.task_name
with Flow("ML-WORKFLOWS-EXAMPLE") as flow:
    bucket_name = Parameter('bucket_name', default='ml-workflows')

    data: dd.DataFrame = IO.read_data(bucket_name=bucket_name, folder_name='in', table_name='example_data')
    
    data: dd.DataFrame = ML.feature_engineering(data=data)
    data: dd.DataFrame = ML.inference(data=data)

    IO.write_to_S3(bucket_name=bucket_name, folder_name='out', table_name='example_data')
    





flow.storage = GitHub( # prefect register -f _flow.py
    repo="Brontomerus/ml-workflows", 
    ref="master",
    path="/workflows/ml/flow.py", 
    secrets=["GITHUB_ACCESS_TOKEN"]
)

flow.run_config = LocalRun(labels=['dev'])


flow.executor = DaskExecutor(
    cluster_class="dask_cloudprovider.aws.FargateCluster",
    cluster_kwargs={
        "image": "daskdev/dask:2021.4.1", 
        "fargate_use_private_ip": True,
        "n_workers": 2,
        "scheduler_timeout": "4 minutes",
        "worker_cpu": 2048, #2048
        "worker_mem": 4096, #8192
        "vpc": Secret("AWS_VPC").get(),
        "cluster_arn": Secret("AWS_FARGATE_CLUSTER_ARN").get(),
        "subnets": [Secret("AWS_ECS_SUBNET").get()],
        "security_groups": [Secret("AWS_SECURITY_GRP_1").get(), Secret("AWS_SECURITY_GRP_2").get(), Secret("AWS_SECURITY_GRP_3").get()],
        "execution_role_arn": Secret("AWS_ECS_TASK_DEFINITION_ARN").get(),
        "task_role_arn": Secret("AWS_ECS_TASK_DEFINITION_ARN").get(),
        "environment":{
            "EXTRA_PIP_PACKAGES": "pip install --no-cache prefect[aws]==0.14.0 prefect[github]==0.14.0 boto3 s3fs pyarrow dask-ml==1.9.0 ",
            # "EXTRA_CONDA_PACKAGES": " --yes -c conda-forge s3fs prefect[aws,github]==0.14.16 pyarrow==3.0.0",
            "AWS_ACCESS_KEY_ID": Secret("AWS_ACCESS_KEY").get(), 
            "AWS_SECRET_ACCESS_KEY": Secret("AWS_SECRET_KEY").get(), 
            "AWS_DEFAULT_REGION": "us-east-2"
        }
    }
)

flow.register("deck-of-dice")

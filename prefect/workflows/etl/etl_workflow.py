from prefect import task, Flow, Parameter
from typing import List
import datetime
import s3fs

import dask.dataframe as dd
import pandas as pd

import prefect 
from prefect.client import Secret



class Extract:
    @staticmethod
    @task
    def storm_details() -> dd.DataFrame:
        """getting table table from NOAA data store"""
        df_storm_details = dd.read_csv("https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_*.csv.gz", compression='gzip', encoding='latin') # , encoding_errors='ignore'
        return data



class Transform:
    @staticmethod
    @task
    def set_col_dtypes(data: dd.DataFrame):
        data['id'] = data['id'].astype(int)
        data['user_id'] = data['user_id'].astype(int)
        data['date'] = data.created.dt.strftime("%Y-%m-%d")
        data = data.persist()
        return data
    
    @staticmethod
    @task
    def date_filter(year: str, month: str, day: str) -> str:
        """create date string for filtering users"""
        return "created >= '" + str(year) + '-' + str(month) + '-' + str(day) + " 00:00:00'" #'2020-12-17'

    @staticmethod
    @task
    def rpu(data: dd.DataFrame) -> pd.DataFrame:
        """calculate the rolls per day"""
        data = data.groupby(['user_id','date']).id.count().reset_index().compute()
        return data



class Load:
    @staticmethod
    @task
    def write_to_s3(data: pd.DataFrame, folder_name: str, table_name: str) -> None:
        data.to_parquet(path=f"s3://btd-analytics-etl/{folder_name}/{table_name}", compression='gzip', engine='pyarrow')
 


with Flow("SIU-BI-DAILY-RPU-DEV") as flow:
    env = Parameter('env', default='')
    year = Parameter('year', default = '2020')
    month = Parameter('month', default = '11')
    day = Parameter('day', default = '25')
    cutoff_date: str = Transform.date_filter(year, month, day)
    # date_str = '20210128'
    
    # extract data
    data: dd.DataFrame = Extract.siu_match_user_round_roll(env=env)

    # transform data & calculate daily rpu
    data: dd.DataFrame = Transform.set_col_dtypes(data=data)
    data: pd.DataFrame = Transform.rpu(data=data)
    
    # write to s3
    Load.write_to_s3(data=data, folder_name='bi', table_name='daily_rpu')
    







from prefect.client import Secret
from prefect.storage.github import GitHub
flow.storage = GitHub( # prefect register -f _flow.py
    repo="Brontomerus/btd-data", 
    ref="dev",
    path="/etl/bi/daily_rpu.py", 
    secrets=["GITHUB_ACCESS_TOKEN"]
)

from prefect.run_configs import LocalRun
flow.run_config = LocalRun(labels=['dev'])

from dask_cloudprovider.aws import FargateCluster
from prefect.executors import DaskExecutor
flow.executor = DaskExecutor(
    cluster_class="dask_cloudprovider.aws.FargateCluster",
    cluster_kwargs={
        "image": "daskdev/dask:2021.2.0", 
        "fargate_use_private_ip": True,
        "n_workers": 2,
        "scheduler_timeout": "6 minutes",
        "worker_cpu": 2048, #2048
        "worker_mem": 8192, #8192
        "vpc": Secret("AWS_VPC").get(),
        "cluster_arn": Secret("AWS_FARGATE_CLUSTER_ARN").get(),
        "subnets": [Secret("AWS_ECS_SUBNET").get()],
        "security_groups": [Secret("AWS_SECURITY_GRP_1").get(), Secret("AWS_SECURITY_GRP_2").get(), Secret("AWS_SECURITY_GRP_3").get()],
        "execution_role_arn": Secret("AWS_ECS_TASK_DEFINITION_ARN").get(),
        "task_role_arn": Secret("AWS_ECS_TASK_DEFINITION_ARN").get(),
        "environment":{
            "EXTRA_PIP_PACKAGES": "pip install --no-cache prefect[aws]==0.14.0 prefect[github]==0.14.0 boto3 s3fs pyarrow",
            # "EXTRA_CONDA_PACKAGES": " --yes -c conda-forge s3fs prefect[aws,github]==0.14.16 pyarrow==3.0.0",
            "AWS_ACCESS_KEY_ID": Secret("AWS_ACCESS_KEY").get(), 
            "AWS_SECRET_ACCESS_KEY": Secret("AWS_SECRET_KEY").get(), 
            "AWS_DEFAULT_REGION": 'us-east-2'
        }
    }
)

flow.register("deck-of-dice")


# # start our Dask cluster
# from dask.distributed import Client,LocalCluster
# from prefect.executors import LocalDaskExecutor

# if __name__ == '__main__':
#     cluster = LocalCluster()
    
#     # point Prefect's DaskExecutor to our Dask cluster
#     with Client(cluster) as client:
#         print("scheduler host: ", client.scheduler.address)
#         executor = LocalDaskExecutor(address=client.scheduler.address)
#         flow.run(executor=executor)



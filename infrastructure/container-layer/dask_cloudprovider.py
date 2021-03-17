from dask_cloudprovider.aws import FargateCluster
from dask.distributed import Client

if __name__ == '__main__':
    cluster = FargateCluster(n_workers = 1,
                        fargate_use_private_ip=True,
                        vpc = ,
                        subnets = [],
                        security_groups=[],
                        cluster_arn = ,
                        execution_role_arn= ,
                        # task_role_arn="" # something with s3 access
                        # image = "", 
                        # environment = {
                            # "EXTRA_CONDA_PACKAGES": "",
                            # ,"EXTRA_PIP_PACKAGES": ""
                        # }
                    )
    with Client(cluster) as client:
        print("scheduler host: ", client.scheduler.address)


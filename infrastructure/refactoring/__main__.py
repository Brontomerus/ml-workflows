import iam
import vpc
import vpn
import dask
import agents
import lb
import pulumi
import pulumi_aws as aws

# this pulumi structure is modeled following this example: https://github.com/pulumi/examples/tree/master/aws-py-eks


config = pulumi.Config()
stack = config.require('environment')

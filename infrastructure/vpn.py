import pulumi
import pulumi_aws as aws


config = pulumi.Config()
stack = config.require('environment')


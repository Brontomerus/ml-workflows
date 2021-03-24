# Infrastructure

There are 4 main layers currently in the infrastructure defined in this project, and are to be deployed in the order they are listed as the later layers are dependent on the earlier layers. 

1.  [network-layer](network-layer/): VPC & Subnets are defined here for the logical security and a foundation to build on. 
2.  [container-layer](container-layer/): ECS Cluster and other required resources.
3.  [loadbalancing-layer](loadbalancing-layer/): Load Balancing resource for the ECS Cluster Containers.
4.  [agent-layer](agent-layer/): Most complicated layer responsible for setting up EC2 containers with SSH access followed by provisioning for our Prefect Agents




# Getting Started

Make sure you have awscli installed and if you have not yet configured your AWS SDK, then run and fill out the required fields:

```bash
$ pip install awscli
...
$ aws configure
AWS Access Key ID [None]: <your access key id here>
AWS Secret Access Key [None]: <your secret key here>
Default region name [None]: us-east-2
Default output format [None]: json
```

If you have multiple AWS profiles (like me), then you'll need to whip up a quick environment variable to avoid messing up and throwing this into the wrong AWS Account... which would __not__ be ideal:
```bash
$ export AWS_PROFILES=my-profile-name
# OR export only the config vars its looking for
$ export AWS_ACCESS_KEY_ID="anaccesskey"
$ export AWS_SECRET_ACCESS_KEY="asecretkey"
$ export AWS_DEFAULT_REGION="us-east-2"
```



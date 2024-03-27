# AWS Infrastructure

This directory is where the AWS resources are defined for the project. These resources are defined, provisioned, and managed via [Pulumi](https://www.pulumi.com/docs/) as my Infrastructure-as-Code of choice.

There are 5 main layers in the stack. They are listed in order of creation, as the network layer must always be created first, followed by the VPN Layer, then the Load Balancing Layer, etc etc... Each of which is described in further detail below:
1. **Network Layer** (network-layer/)
2. **VPN Layer** (vpn-layer/)
3. **Load Balancing Layer** (loadbalancing-layer/)
4. **Container Layer** (container-layer/)
5. **Agent Layer** (agent-layer/)

<br>
This architecture works great for the system I'm building here, because it allows for flexibility and reusablility when it comes to certain components. By adjusting the scripts, I can (and will) launch prefect agents to launch either dev or prod workflows, which enhances my control over the environment at the same time as allowing me to limit the need for needlessly replicating services and clusters in separate, isolated environments.


### Network Layer
The network layer defines the VPC that will house our environment. This layer contains the logic for our network and much of the basic security that underlies the rest of the resources to come. It includes things like public subnets, private subnets, NAT Gateways, Internet Gateways, Security Groups, and routing tables. Think of it as the base layer of our architecture, and will serve as the main building block which will be referenced in later stacks.

### VPN Layer
This layer is for the less-than-fun stuff if you're not a network engineer, but a vital and necessary one. We need to access our resources and kick clusters off for building and training our model, which requires that we are able to directly and securely access the resources to do so. 

**NOTE** - I have not fully created all the necessary components, and continue to work to create acceptable security. The features to be added are Active Directory & MFA so we can assure our resources are protected by all means available.

### Load Balancing Layer
Load Balancing is important for the ECS Clusters, as well as other resources to be built.

### Container Layer
Where Dask eats and sleeps. This defines our ECS resources for use with Dask-CloudProvider, which calls for a cluster capable of spinning up & down as needed. This includes the security groups and other networking resources that fall into consideration when assuming the needs for the scheduler node to properly communicate with the worker nodes.

### Agent Layer
Prefect Agents need to live somewhere too. I prefer to separate the agent containers from the dask containers because it makes for a much more explicitly defined environment. These are defined a bit differently than the dask container-layer, because instead of relying on temporary services, we must define a service to manage our custom tasks which are defined in this layer. Therefore, this layer will resemble a much more fully defined ECS Cluster when compared to the dask layer.

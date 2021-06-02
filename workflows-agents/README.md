# Prefect Agents

As defined in infrastructure, we'll need to spin up some [Prefect Agents](https://docs.prefect.io/orchestration/agents/overview.html) in order to set our orchestration up in our AWS account.


# What are Prefect Agents, and How to Use Them?

Prefect Agents are small applications that come packaged in the Prefect python library when you pip install. To be straightforward, all agents do is simply send API requests to Prefect Cloud and query your Prefect Cloud account for any pending flows to run. The agent architecture follows what Prefect dubbed the [Hybrid Execution Model](https://medium.com/the-prefect-blog/the-prefect-hybrid-model-1b70c7fd296), and is what I'd say is their "special sauce". These can be spun up via code or via the CLI depending on how you want to spin them up, and are very simple to configure. I am using AWS ECS+Fargate to host these because I don't have any time to continously manage and patch servers, so serverless is the best option for me.




# Workflows

Roughly speaking, workflows are units of work that define a given set of functions - or tasks - that are to be applied on a given set of inputs. The workflows also encapsulate the *where* and *how* for running the aforementioned tasks. This falls into the realm of things you might call **DevOps**, **MLOps**, or even **orchestration**. These workflows will essentially represent a chunk of all three, but with an emphasis on **Orchestration**.
<br>

To define, schedule, manage, and run our code, I am going to use a combination of [Prefect]() and [Dask](). Prefect is an orchestration tool, akin to Airflow and AWS Steps. Dask is essentially how we define our environment and how we distribute our computation across several nodes, or servers, in a predefined cluster. Dask is also how we will spin up temporary clusters in this example, and thus will provide a degree of "DevOps" in our stack here as well.

# Prefect

Prefect revolves around 3 main components:
- Storage
- Run Configuration
- Executor
<br>

For this project, I will be using a combination that I find ideal for smaller workshops that provides a low-cost approach but delivers powerful and highly capable analytical toolset. The following sections define the subject matter a bit more in depth, and describes my choices a bit more.

### Storage
The storage is essentially the _where_ our code lives. Where our code lies is an incredibly important consideration for DevOps, as it can effect everything downstream. Luckily, Prefect has more than a few ways to approach this. I'm not going to dive into the internals here, as most other options would take a while to cover, but know that you can readily access them [here](https://docs.prefect.io/orchestration/flow_config/storage.html).
<br>

My choice: **Github**
<br>

GitHub storage is my favorite because it's a pretty intuitive way to handle your flows. You simply code them and deploy them. No intermediary Docker builds and other nonsense, just straight to business. It's also nice and quick - requiring less resources that we ultimately need to set up, which is always a win.

### Run Configuration
Run Configurations pertain to how our Agents access and run our defined flows. 
<br>

My choice: **ECS**
<br>
The reason here should be reasonably obvious given the stack we are working with. This agent gives us the ability to serve our agent directly to the correct environment and executor that we'll be using.

### Executor
Executors define your environment. Prefect is fairly reliant on Dask, but this is also where we can do something I personally think is amazing: temporary clusters. The cluster is spun up on demand and automatically retired following execution of the flow - pass or fail.
<br>

My choice: **DaskExecutor using Dask-CloudProvider**
<br>
The use of the DaskExecutor was a given, but something that warrants more documentation is the use of Dask-CloudProvider as a means for temporary cluster creation. This is an awesome way to approach the problem at hand, because it allows us some flexibility, but more importantly it saves us cash. This is always #1, because a product that costs too much makes margin that much slimmer. In a data science project, that margin might be fractions of a penny, and if you scale up with a negative margin then you've got some trouble on your hands.


# Putting an ML Model to Work

My example workflow is primarily based on putting the Machine Learning model created & serialized in the /ml-models directory into a batch workflow - best for taking that ML model and running loads of upwards of 500 GB through at one time. 

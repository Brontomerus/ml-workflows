# Workflows

Roughly speaking, workflows are units of work that define a given set of functions - or tasks - that are to be applied on a given set of inputs. The workflows also encapsulate the *where* and *how* for running the aforementioned tasks. This falls into the realm of things you might call **DevOps**, **MLOps**, or even **orchestration**. These workflows will essentially represent a chunk of all three, but with an emphasis on **Orchestration**.
<br>

To define, schedule, manage, and run our code, I am going to use a combination of [Prefect]() and [Dask](). Prefect is an orchestration tool, akin to Airflow and AWS Steps. Dask is essentially how we define our environment and how we distribute our computation across several nodes, or servers, in a predefined cluster. Dask is also how we will spin up temporary clusters in this example, and thus will provide a degree of "DevOps" in our stack here as well.

# Prefect

# ml-workflows

A project to provide an easy way to get started building distributed environments for machine learning workflows in AWS using [__Prefect__](https://www.prefect.io/) for dataflow automation capabilities (scheduling, CI/CD, ETL Framework, etc) and [__Dask__](https://docs.dask.org/en/latest/why.html) for a providing distributed compute engine. This work is facilitated by managed python environments using [__Poetry__](https://python-poetry.org/docs/basic-usage/) for package management and [__Pulumi__](https://www.pulumi.com/docs/) for defining the cloud architecture using Infrastructure-as-Code. Further, I leverage [__Dask-CloudProvider__](https://cloudprovider.dask.org/en/latest/) to further add to the IaC capabilities and to easily harness the phenomenal "temporary cluster" approach that I've come to absolutely love for its low-cost but high-performance serverless capabilities.

Using a pythonic approach, I want to build a bootstrap resource for enabling anyone to quickly get started using Dask and Prefect for distributed data processing and operatiing ML resources in cloud environments. I have created a process within an AWS environment for a separate company I worked for, but wanted to then create another project for a separate company following a similar approach. To enable adoption of this awesome tech stack, I decided to embark on a project that will enable others to follow a similar approach with ease, as well as allowing myself a project to build off for other endeavors of mine.

The idea is to use Pulumi Infrastructure-as-Code (IaC) to define and manage a serverless infrastructure in AWS, which can then be utilized with Prefect and Dask. I am using Poetry for package management within the workflows folder to enable a smoother process to get started. There are 2 main directories in this project:

1. [infrastructure/](infrastructure/): The IaC for quickly building the required infrastructure in an AWS cloud environment.
2. [workflows/](workflows/): The modeling examples as well as the prefect workflow logic.



# Architecture

The project architecture is defined as Pulumi Infrastructure-as-Code (IaC), and runs on an AWS environment. 



# Modeling

This isn't your grandpa's scikit-learn model, but (but sklearn _is_ a fantastic and ellegant data science library). I used dask-ml to build my feature engineering and predictive model for this project to demonstrate a scalable approach you could take to deploy a model using this framework. The folks at pydata working on scikit-learn are a heck of a lot smarter than most people regarding the data science ecosystem, and there's a reason they began building Dask. While scikit-learn is fast, highly diversified, and portable, dask-ml is certainly a bit more rigid. The reason for using dask-ml is simply that it allows us an easy way to __scale__ our model to serve very large batch sizes. GB of records? Try PB of records! 

Other ways to build scalable models are certainly out there, namely in Spark ML. Spark ML is easily combined with PySpark to build scalable infrastructure on the ever-popular Apache Spark, and I couldn't talk all about dask/dask-ml without mentioning that alternative. At the end of the day, do what you are the most comfortable with supporting - because systems almost _always_ live much longer at your company than the people who build them.


# Getting Started
There are a few initial requirements to sort out before you get going here. A few basic things you need to set up/install to get rolling:

1. Install [Python](https://www.python.org/downloads/) 3.8+ ... I wrote this using Python 3.8.5 installed locally, but anything in the 3.8.X range should work. Note: This is more relaxed than the Docker environments for Dask, which is _very_ important that you have the same version across those containers and your environment, or random hard-to-debug problems will arise.
2. Install [Docker](https://docs.docker.com/get-docker/) on your computer.
3. Install [Poetry](https://python-poetry.org/docs/) on your computer.
4. Install [Pulumi](https://www.pulumi.com/docs/get-started/aws/begin/), and make an account.



# Last Remark

One might be inclined to say, "That model is hot garbage, this guy has no idea what he's doing!".

Yes, the actual model is probably some hot garbage and would ultimately be wrong enough that it would lose you money if you were to test its merits in the market. While I enjoyed the modeling part of this project, it was perhaps substantially less detailed than the architectural considerations in this project. The modeling aspect really came last in my focus on this project because I really wanted to focus on _where_ the code was running and less on _what_ the code was running on this project. While the ROI and predictive quality of a model will usually come first for a business when debating whether to build something like this, I wanted to focus on making this a reusable base-template for future use. Thus, the architectural components and the ease of reproducing those components came first for this project, whereas the model(s) that are run on it are destined to change given the exact problem the business is trying to solve.



# About the Author

Hi, I'm Brandon. I like data science and data analytics in all shapes and sizes. I also like building things, which is how and why I found myself pushing myself to learn all these neat things. I found the Python community, as well as the data science subset of the Python community very welcoming. One thing that has begun to be very clear, is that an often neglected 



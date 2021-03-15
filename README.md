# ml-werkflows
A project to provide an easy way to get started building distributed environments for machine learning workflows in AWS using Prefect and Dask.

Using a pythonic approach, I want to build a bootstrap resource for enabling anyone to quickly get started using Dask and Prefect for distributed data processing and operatiing ML resources in cloud environments. I have created a process within an AWS environment for a separate company I worked for, but wanted to then create another project for a separate company following a similar approach. To enable adoption of this awesome tech stack, I decided to embark on a project that will enable others to follow a similar approach with ease, as well as allowing myself a project to build off for other endeavors of mine.

The idea is to use Pulumi Infrastructure-as-Code (IaC) to define and manage a serverless infrastructure in AWS, which can then be utilized with Prefect and Dask. I am using Poetry for package management within the workflows folder to enable a smoother process to get started. There are 2 main directories in this project:

1. [infrastructure/](infrastructure/): The IaC for quickly building the required infrastructure in an AWS cloud environment.
2. [workflows/](workflows/): The modeling examples as well as the prefect workflow logic.



# About the Author

Hi, I'm Brandon. I like data analytics in all shapes and sizes.



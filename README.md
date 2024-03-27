# ml-workflows 

ml-workflows is my personal project to demonstrate usage of analytics platforms I've found interest in. The main directories are now focused on usage of Databricks, but I've also archived past work on a system which leverged Prefect and Dask Cloud Provider to process data in a cloud cluster compute environment. This repository serves as my monorepo to build and learn so you will find a few projects in a few different directories:

## databricks/
1. [terraform/](databricks/terraform/): AWS (And maybe Azure at some point?) Infra using Terraform.
2. [analytics/](databricks/analytics/): Databricks Code for ETL, DDL, and all the other fun stuff.

(Note, I wouldn't want my Databricks repo to have this depth - the UI is fairly slow when navigating the code)

## api/
Example FastAPI implementation and Docker build to encapsulate and deploy as an image.

## prefect/
Archived project built prior to Prefect's overhaul and API alterations.




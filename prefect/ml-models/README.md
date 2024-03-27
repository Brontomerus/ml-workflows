# Predictive Modeling

This project will make use of data from Deck of Dice Gaming, a startup I currently work for in my spare time that conceptualizes and produces mobile games. The data I've actually modelled on is stored in a secure account and requires authentication to retrieve. Because of this, I have created a separate dataset with matching columns and types, but have filled it with randomized and useless data. To fully implement this project, you'll need to copy this data into an S3 bucket created in the pulumi code named 

**need to put this in later !!!!!!!!!!!!!!!!!!!!!! __________________________ **

# About This Directory

This directory in the monorepo is for building our predictive models for use in the workflows part of the project. To have an advanced approach to our MLOps, there are a few important features to focus on here:

1. The serialized models must be versionable.
    - Automation for testing model decay.
    - Automation for re-training the model when the predictiveness decays past a certain defined threshold.
2. The data will be stored within AWS S3, in parquet files. You will need to load those given files into the defined S3 bucket for a dry run.
3. ...

< under construction >
# Databricks notebook source
import json
from multiprocessing.pool import ThreadPool

# COMMAND ----------

orchestration = spark.sql("select * from utility.orchestration.merge").toPandas().to_dict(orient = 'records')
# orchestration

# COMMAND ----------

# Set the ThreadPool to the # of Nodes because the data isn't so large
pool = ThreadPool(6)

# COMMAND ----------

pool.map(lambda params: dbutils.notebook.run("../extract/_merge", timeout_seconds= 3600, arguments=params), orchestration)

# Databricks notebook source
dbutils.widgets.text("catolog", defaultValue="wrangled")
dbutils.widgets.text("schema", defaultValue="extracts")
dbutils.widgets.text("table", defaultValue="")
dbutils.widgets.dropdown("_safety", defaultValue="DONT RUN", choices=['RUN','DONT RUN'])

if dbutils.widgets.get('catolog') != 'wrangled':
    catalog_path = f"s3://analytics-btd-curated/{dbutils.widgets.get('catolog')}/{dbutils.widgets.get('schema')}/{dbutils.widgets.get('table')}"
else:
    catalog_path = f"s3://analytics-btd-{dbutils.widgets.get('catolog')}/{dbutils.widgets.get('schema')}/{dbutils.widgets.get('table')}"

# COMMAND ----------

if dbutils.widgets.get('_safety') == 'RUN':
    spark.sql(f"DROP TABLE IF EXISTS {dbutils.widgets.get('catolog')}.{dbutils.widgets.get('schema')}.{dbutils.widgets.get('table')}")
    print(dbutils.fs.rm(catalog_path, recurse=True))
else:
    print("DONT RUN is currently selected. Table not dropped!")

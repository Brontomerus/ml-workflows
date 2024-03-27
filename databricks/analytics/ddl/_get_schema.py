# Databricks notebook source
dbutils.fs.ls(f"s3://btd-db-archive/db-table-backup-yyyymmdd/extracts/")

# COMMAND ----------

import pyspark.pandas as ps
import datetime
import pyspark
from pytz import timezone


mapper = {
    'object': 'STRING',
    'int64': 'INT',
    'int32': 'INT',
    'int16': 'INT',
    'int8': 'INT',
    'datetime64[ns]': 'TIMESTAMP',
    'float64': 'DECIMAL(30,2)',
    'float32': 'DECIMAL(30,2)',
    'bool': 'BOOLEAN'
}

df = ps.read_parquet(f"s3://btd-db-archive/db-table-backup-{datetime.datetime.now(timezone('EST')).strftime('%Y%m%d')}}/extracts/extracts.example/1/*.gz.parquet")
for col in df.columns:
    print(f"{col}       {mapper[str(df[col].dtype)]}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- show create table wrangled.raw.wallet_transaction_key
# MAGIC SELECT from_unixtime(0, 'yMM');

# COMMAND ----------



# Databricks notebook source
import datetime
import json
import pyspark
from pytz import timezone

dbutils.widgets.text("tbl", defaultValue="")
dbutils.widgets.text("bucket", defaultValue="btd-db-archive")
dbutils.widgets.text("root_folder", defaultValue=f"db-table-backup-{datetime.datetime.now(timezone('EST')).strftime('%Y%m%d')}")
dbutils.widgets.text("stem", defaultValue="extracts/extracts.")
dbutils.widgets.text("path_suffix", defaultValue="/1/")
dbutils.widgets.text("merge_keys_equal", defaultValue="")
dbutils.widgets.text("merge_keys_not_equal", defaultValue="")
dbutils.widgets.text("updated_column_check", defaultValue="")

table = dbutils.widgets.get('tbl')
bucket = dbutils.widgets.get('bucket')
root_folder = dbutils.widgets.get('root_folder')
stem = dbutils.widgets.get('stem')
path_suffix = dbutils.widgets.get('path_suffix')
merge_keys_equal = dbutils.widgets.get('merge_keys_equal').split(',')
merge_keys_not_equal = dbutils.widgets.get('merge_keys_not_equal').split(',')
updated_column_check = dbutils.widgets.get('updated_column_check')

# COMMAND ----------

path = f"s3://{bucket}/{root_folder}/{stem}{table}{path_suffix}"

# COMMAND ----------

# Create or Replace the table at the given path
dbutils.notebook.run("../../ddl/wrangled/raw.dynamic", 600, {"LOCATION": path, "TBL": table})

# COMMAND ----------

merge_keys_str_list = []
for k in merge_keys_equal:
    if k != '':
        merge_keys_str_list.append(f"target.{k} = source.{k}")
for k in merge_keys_not_equal:
    if k != '':
        merge_keys_str_list.append(f"target.{k} <> source.{k}")

# COMMAND ----------

# columns list
columns=spark.sql(f"select * from wrangled.raw.{table} limit 0").columns
update_list, insert_list = [],[]
for col in columns:
    col = col.strip()
    update_list.append(f"\n  target.{col} = source.{col}")
    insert_list.append(f"source.{col}")


# COMMAND ----------

merge_sql = f"""
MERGE INTO wrangled.extracts.{table} target USING wrangled.raw.{table} source
ON {' AND '.join([s.replace(' ', '') for s in merge_keys_str_list])}
WHEN MATCHED {updated_column_check} THEN UPDATE SET {','.join(update_list)}
WHEN NOT MATCHED THEN 
 INSERT ({','.join(columns)}) 
 VALUES ({','.join(insert_list)}) 
""".strip()
print(merge_sql)

# COMMAND ----------

out = spark.sql(merge_sql).toPandas().to_json(orient = 'records')
dbutils.notebook.exit(json.dumps(out))

-- Databricks notebook source
-- MAGIC %python
-- MAGIC spark.sql(f"DROP TABLE IF EXISTS utility.orchestration.merge")

-- COMMAND ----------

CREATE TABLE utility.orchestration.merge (
  tbl                    STRING COMMENT 'Table Name in extracts source database',
  bucket                 STRING DEFAULT 'btd-db-archive' COMMENT 'bucket for wrangled.raw tables',
--   root_folder            STRING DEFAULT NULL COMMENT 'root folder for wrangled.raw tables',
  stem                   STRING DEFAULT 'extracts/extracts.' COMMENT 'folder stem for wrangled.raw tables',
  path_suffix            STRING DEFAULT '/1/' COMMENT 'end path in parquet for raw source',
  merge_keys_equal       STRING COMMENT 'merge keys for a table that are =',
  merge_keys_not_equal   STRING DEFAULT '' COMMENT 'merge keys for a table that are <>',
  updated_column_check   STRING DEFAULT '' COMMENT 'sql statement for merge conditional stmt')
USING JSON
LOCATION 's3://analytics-btd-curated/utility/orchestration/merge'

-- COMMAND ----------

INSERT INTO utility.orchestration.merge 
(tbl, merge_keys_equal, merge_keys_not_equal, updated_column_check)
VALUES 
(
  "table1",
  "user_id, platform_id, site_id",
  "",
  ""
),
(
  "table2",
  "id, id2",
  "",
  "AND source.updated > target.updated"
),
(
  "table3",
  "id",
  "",
  "AND source.updated > target.updated"
)


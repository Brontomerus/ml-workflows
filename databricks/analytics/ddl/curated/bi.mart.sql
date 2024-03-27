-- Databricks notebook source
CREATE OR REPLACE VIEW bi.mart.users
--   (id COMMENT 'Unique identification number', Name)
AS SELECT 
    1 as user_id
    'hello world' as user
-- COMMAND ----------

CREATE TABLE bi.mart.example(
	user_id                 STRING,
    create_date             DATE,
    metric                  INT
USING DELTA
LOCATION 's3://analytics-btd-curated/bi/mart/example'
TBLPROPERTIES (
  delta.autoOptimize.optimizeWrite = true,
  delta.autoOptimize.autoCompact = true)


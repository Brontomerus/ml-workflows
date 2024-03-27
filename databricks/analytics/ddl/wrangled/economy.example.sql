-- Databricks notebook source
CREATE TABLE wrangled.extracts.example (
  user_id                 STRING,
  create_date             DATE,
  metric                  INT
  )
USING DELTA
LOCATION 's3://analytics-btd-wrangled/economy/example'
TBLPROPERTIES (
  delta.autoOptimize.optimizeWrite = true, 
  delta.autoOptimize.autoCompact = true)

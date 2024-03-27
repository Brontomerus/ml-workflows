-- Databricks notebook source
CREATE TABLE wrangled.raw.wallet_transaction_amount AS (
    uuid STRING,
    stuff STRING,
    quantity INT,
    created TIMESTAMP,
    updated TIMESTAMP,
    user INT,
    transaction_yrmnth STRING
)
USING DELTA
LOCATION
    's3://analytics-btd-curated/wrangled/raw/example'
PARTITION BY (
    transaction_yrmnth
)



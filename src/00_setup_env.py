# Databricks notebook source
# MAGIC %md
# MAGIC # 00 - Setup Environment
# MAGIC Creates/validates catalog + schema and defines shared table names for Bronze layer.

# COMMAND ----------

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Update these defaults in Databricks as needed
CATALOG = "main"
SCHEMA = "health_equity_capstone"

BRONZE_CDC_PLACES_TABLE = f"{CATALOG}.{SCHEMA}.bronze_cdc_places"
BRONZE_ACS_TABLE = f"{CATALOG}.{SCHEMA}.bronze_census_acs"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")

print("Environment ready")
print(f"Catalog: {CATALOG}")
print(f"Schema:  {SCHEMA}")
print(f"CDC table: {BRONZE_CDC_PLACES_TABLE}")
print(f"ACS table: {BRONZE_ACS_TABLE}")

# Databricks notebook source
# MAGIC %md
# MAGIC # 00 - Setup Environment
# MAGIC Creates/validates catalog + schema and defines shared table names for Bronze layer.

# COMMAND ----------



from pyspark.sql import SparkSession
from config import (
    ACS_SOURCE_PATH,
    BRONZE_ACS_TABLE,
    BRONZE_CDC_PLACES_TABLE,
    CATALOG,
    CDC_PLACES_SOURCE_PATH,
    DOCS_SOURCE_PATH,
    SCHEMA,
)

spark = SparkSession.builder.getOrCreate()

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")

# Managed UC Volumes (default).
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{SCHEMA}.cdc_places")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{SCHEMA}.census_acs")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{SCHEMA}.cdc_who_docs")

# External volume pattern (future option):
# spark.sql(f\"CREATE EXTERNAL VOLUME IF NOT EXISTS {CATALOG}.{SCHEMA}.cdc_places LOCATION 's3://<bucket>/cdc_places'\")
# spark.sql(f\"CREATE EXTERNAL VOLUME IF NOT EXISTS {CATALOG}.{SCHEMA}.census_acs LOCATION 's3://<bucket>/census_acs'\")

print("Environment ready")
print(f"Catalog: {CATALOG}")
print(f"Schema:  {SCHEMA}")
print(f"CDC table: {BRONZE_CDC_PLACES_TABLE}")
print(f"ACS table: {BRONZE_ACS_TABLE}")
print(f"Landing spot for raw CDC PLACES data: {CDC_PLACES_SOURCE_PATH}")
print(f"Landing spot for raw ACS data: {ACS_SOURCE_PATH}")
print(f"Landing spot for raw CDC/WHO docs: {DOCS_SOURCE_PATH}")
display(spark.sql(f"SHOW VOLUMES IN {CATALOG}.{SCHEMA}"))

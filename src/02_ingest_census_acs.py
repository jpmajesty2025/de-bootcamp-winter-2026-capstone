# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Ingest Census ACS to Bronze
# MAGIC Reads Census ACS extract and lands raw records with ingestion metadata.

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit

spark = SparkSession.builder.getOrCreate()

from config import ACS_SOURCE_PATH, BRONZE_ACS_TABLE, ACS_SOURCE_FILE

raw_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{ACS_SOURCE_PATH}{ACS_SOURCE_FILE}")
)

bronze_df = (
    raw_df
    .withColumn("ingestion_ts", current_timestamp())
    .withColumn("source_path", lit(f"{ACS_SOURCE_PATH}{ACS_SOURCE_FILE}"))
    .withColumn("source_system", lit("census_acs"))
)

(
    bronze_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(BRONZE_ACS_TABLE)
)

print(f"Wrote ACS Bronze rows to {BRONZE_ACS_TABLE}: {bronze_df.count()}")

# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Ingest CDC PLACES to Bronze
# MAGIC Reads CDC PLACES CSV/API extract and lands raw records with ingestion metadata.

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit

spark = SparkSession.builder.getOrCreate()

from config import BRONZE_CDC_PLACES_TABLE, CDC_PLACES_SOURCE_PATH,CDC_PLACES_SOURCE_FILE

raw_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{CDC_PLACES_SOURCE_PATH}{CDC_PLACES_SOURCE_FILE}")
)

bronze_df = (
    raw_df
    .withColumn("ingestion_ts", current_timestamp())
    .withColumn("source_path", lit(f"{CDC_PLACES_SOURCE_PATH}{CDC_PLACES_SOURCE_FILE}"))
    .withColumn("source_system", lit("cdc_places"))
)

(
    bronze_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(BRONZE_CDC_PLACES_TABLE)
)

print(f"Wrote CDC PLACES Bronze rows to {BRONZE_CDC_PLACES_TABLE}: {bronze_df.count()}")

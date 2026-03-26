# Databricks notebook source
# MAGIC %md
# MAGIC # 03 - Validate Bronze Tables
# MAGIC Validates CDC and ACS Bronze table writes, row counts, and ingestion metadata presence.

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from config import BRONZE_ACS_TABLE, BRONZE_CDC_PLACES_TABLE

spark = SparkSession.builder.getOrCreate()


def validate_table(table_name: str, table_label: str) -> None:
    print(f"\n--- Validating {table_label}: {table_name} ---")

    if not spark.catalog.tableExists(table_name):
        raise ValueError(f"Table does not exist: {table_name}")

    df = spark.table(table_name)
    row_count = df.count()

    if row_count == 0:
        raise ValueError(f"Table has 0 rows: {table_name}")

    required_cols = ["ingestion_ts", "source_path", "source_system"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in {table_name}: {missing}")

    null_meta_count = df.filter(
        col("ingestion_ts").isNull()
        | col("source_path").isNull()
        | col("source_system").isNull()
    ).count()

    print(f"Rows: {row_count}")
    print(f"Null metadata rows: {null_meta_count}")

    if null_meta_count > 0:
        raise ValueError(f"Found rows with null metadata in {table_name}: {null_meta_count}")

    print("Validation status: PASS")


validate_table(BRONZE_CDC_PLACES_TABLE, "CDC Bronze")
validate_table(BRONZE_ACS_TABLE, "ACS Bronze")

print("\nAll Bronze validations passed.")

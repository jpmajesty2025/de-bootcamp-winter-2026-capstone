# Databricks notebook source
# MAGIC %md
# MAGIC # 05 - Build Gold Health Equity Fact Table
# MAGIC Joins conformed Silver clean tables into a Gold analytical fact for dashboard and agent use.

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when

from config import (
    GOLD_HEALTH_EQUITY_STATS_TABLE,
    SILVER_HEALTH_OUTCOMES_CLEAN_TABLE,
    SILVER_SOCIOECONOMIC_CLEAN_TABLE,
)

spark = SparkSession.builder.getOrCreate()

health_df = spark.table(SILVER_HEALTH_OUTCOMES_CLEAN_TABLE)
socio_df = spark.table(SILVER_SOCIOECONOMIC_CLEAN_TABLE)

gold_df = (
    health_df.alias("h")
    .join(socio_df.alias("s"), on="county_fips", how="inner")
    .select(
        col("county_fips"),
        col("h.year").alias("health_year"),
        col("h.state_abbr"),
        col("h.state_name"),
        col("h.county_name"),
        col("h.measure_id"),
        col("h.measure_name"),
        col("h.data_value"),
        col("s.acs_year"),
        col("s.poverty_pct"),
        col("s.median_household_income"),
        col("h.source_system").alias("health_source_system"),
        col("s.source_system").alias("socio_source_system"),
        col("h.ingestion_ts").alias("health_ingestion_ts"),
        col("s.ingestion_ts").alias("socio_ingestion_ts"),
    )
    .withColumn(
        "health_burden_band",
        when(col("data_value") >= 30, lit("very_high"))
        .when(col("data_value") >= 20, lit("high"))
        .when(col("data_value") >= 10, lit("moderate"))
        .otherwise(lit("low")),
    )
    .withColumn(
        "poverty_band",
        when(col("poverty_pct") >= 20, lit("high_poverty"))
        .when(col("poverty_pct") >= 12, lit("moderate_poverty"))
        .otherwise(lit("lower_poverty")),
    )
)

(
    gold_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(GOLD_HEALTH_EQUITY_STATS_TABLE)
)

print(f"Wrote Gold rows: {gold_df.count()} -> {GOLD_HEALTH_EQUITY_STATS_TABLE}")
print(f"Distinct counties: {gold_df.select('county_fips').distinct().count()}")
print(f"Distinct measures: {gold_df.select('measure_id').distinct().count()}")

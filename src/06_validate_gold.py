# Databricks notebook source
# MAGIC %md
# MAGIC # 06 - Validate Gold Layer
# MAGIC Validates Gold table integrity and writes run-level validation summary metrics.

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, current_timestamp, lit, round as spark_round, when

from config import (
    GOLD_DQ_SUMMARY_TABLE,
    GOLD_HEALTH_EQUITY_STATS_TABLE,
    SILVER_HEALTH_OUTCOMES_CLEAN_TABLE,
)

spark = SparkSession.builder.getOrCreate()

gold_df = spark.table(GOLD_HEALTH_EQUITY_STATS_TABLE)
silver_health_df = spark.table(SILVER_HEALTH_OUTCOMES_CLEAN_TABLE)

gold_row_count = gold_df.count()
if gold_row_count == 0:
    raise ValueError(f"Gold validation failed: 0 rows in {GOLD_HEALTH_EQUITY_STATS_TABLE}")

null_key_metric_rows = gold_df.filter(
    col("county_fips").isNull()
    | col("measure_id").isNull()
    | col("data_value").isNull()
    | col("poverty_pct").isNull()
).count()
if null_key_metric_rows > 0:
    raise ValueError(
        f"Gold validation failed: {null_key_metric_rows} rows have null key metric columns "
        f"in {GOLD_HEALTH_EQUITY_STATS_TABLE}"
    )

# Compare DIABETES average on like-for-like population:
# Gold is an inner-join subset, so Silver must be restricted to Gold counties for a fair check.
gold_diabetes_df = (
    gold_df.filter(col("measure_id") == "DIABETES")
    .select("county_fips", col("data_value").alias("gold_data_value"))
)

silver_diabetes_join_aligned_df = (
    silver_health_df.filter(col("measure_id") == "DIABETES")
    .select("county_fips", col("data_value").alias("silver_data_value"))
    .join(gold_diabetes_df.select("county_fips").distinct(), on="county_fips", how="inner")
)

gold_diabetes_avg = (
    gold_diabetes_df
    .agg(spark_round(avg(col("gold_data_value")), 6).alias("gold_diabetes_avg"))
    .collect()[0][0]
)

silver_diabetes_avg = (
    silver_diabetes_join_aligned_df
    .agg(spark_round(avg(col("silver_data_value")), 6).alias("silver_diabetes_avg"))
    .collect()[0][0]
)

if gold_diabetes_avg is None or silver_diabetes_avg is None:
    diabetes_avg_diff = None
else:
    diabetes_avg_diff = abs(float(gold_diabetes_avg) - float(silver_diabetes_avg))

if diabetes_avg_diff is not None and diabetes_avg_diff > 0.0001:
    raise ValueError(
        f"Gold validation failed: DIABETES average mismatch on join-aligned population "
        f"(gold={gold_diabetes_avg}, silver_join_aligned={silver_diabetes_avg}, diff={diabetes_avg_diff})"
    )

summary_df = (
    spark.createDataFrame(
        [
            (
                "gold",
                "health_equity_stats",
                gold_row_count,
                null_key_metric_rows,
                float(gold_diabetes_avg) if gold_diabetes_avg is not None else None,
                float(silver_diabetes_avg) if silver_diabetes_avg is not None else None,
                float(diabetes_avg_diff) if diabetes_avg_diff is not None else None,
            )
        ],
        [
            "layer",
            "dataset",
            "rows_total",
            "rows_null_key_metrics",
            "gold_diabetes_avg",
            "silver_diabetes_avg",
            "diabetes_avg_diff",
        ],
    )
    .withColumn(
        "status",
        when(col("rows_total") <= 0, lit("FAIL"))
        .when(col("rows_null_key_metrics") > 0, lit("FAIL"))
        .when(col("diabetes_avg_diff").isNotNull() & (col("diabetes_avg_diff") > 0.0001), lit("FAIL"))
        .otherwise(lit("PASS")),
    )
    .withColumn("run_ts", current_timestamp())
)

(
    summary_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(GOLD_DQ_SUMMARY_TABLE)
)

print(f"Gold row count: {gold_row_count}")
print(f"Rows with null key metrics: {null_key_metric_rows}")
print(f"Gold DIABETES avg: {gold_diabetes_avg}")
print(f"Silver DIABETES avg: {silver_diabetes_avg}")
print(f"DIABETES avg diff: {diabetes_avg_diff}")
print(f"Validation summary appended -> {GOLD_DQ_SUMMARY_TABLE}: {summary_df.count()}")
print("Gold validation status: PASS")

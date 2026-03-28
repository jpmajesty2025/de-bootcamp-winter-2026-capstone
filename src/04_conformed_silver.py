# Databricks notebook source
# MAGIC %md
# MAGIC # 04 - Build Conformed Silver Tables (with Quarantine + DQ Monitoring)
# MAGIC Normalizes Bronze CDC/ACS data into conformed Silver outputs, splits clean vs quarantine,
# MAGIC and logs run-level DQ monitoring metrics.

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    array,
    array_remove,
    col,
    concat_ws,
    current_timestamp,
    length,
    lit,
    lpad,
    trim,
    upper,
    when,
)

from config import (
    BRONZE_ACS_TABLE,
    BRONZE_CDC_PLACES_TABLE,
    DQ_MONITORING_TABLE,
    SILVER_HEALTH_OUTCOMES_CLEAN_TABLE,
    SILVER_HEALTH_OUTCOMES_QUARANTINE_TABLE,
    SILVER_HEALTH_OUTCOMES_TABLE,
    SILVER_SOCIOECONOMIC_CLEAN_TABLE,
    SILVER_SOCIOECONOMIC_QUARANTINE_TABLE,
    SILVER_SOCIOECONOMIC_TABLE,
)

spark = SparkSession.builder.getOrCreate()


def with_failed_rules(*rule_exprs):
    return concat_ws(";", array_remove(array(*rule_exprs), lit(None)))


# --- CDC PLACES -> Silver Health Outcomes ---
cdc_bronze_df = spark.table(BRONZE_CDC_PLACES_TABLE)

cdc_conformed_df = (
    cdc_bronze_df
    .withColumn("county_fips", lpad(trim(col("LocationID").cast("string")), 5, "0"))
    .withColumn("measure_id", upper(trim(col("MeasureId"))))
    .withColumn("measure_name", trim(col("Measure")))
    .withColumn("data_value", col("Data_Value").cast("double"))
    .withColumn("year", col("Year").cast("int"))
    .withColumn("state_abbr", trim(col("StateAbbr")))
    .withColumn("state_name", trim(col("StateDesc")))
    .withColumn("county_name", trim(col("LocationName")))
    .withColumn("source_system", col("source_system"))
    .withColumn("source_path", col("source_path"))
    .withColumn("ingestion_ts", col("ingestion_ts"))
    .select(
        "county_fips",
        "year",
        "state_abbr",
        "state_name",
        "county_name",
        "measure_id",
        "measure_name",
        "data_value",
        "source_system",
        "source_path",
        "ingestion_ts",
    )
)

cdc_flagged_df = (
    cdc_conformed_df
    .withColumn(
        "dq_failed_rules",
        with_failed_rules(
            when((col("county_fips").isNull()) | (length(col("county_fips")) != 5), lit("invalid_county_fips")),
            when(col("data_value").isNull(), lit("null_data_value")),
            when((col("data_value") < 0) | (col("data_value") > 100), lit("data_value_out_of_range_0_100")),
            when(col("measure_id").isNull() | (trim(col("measure_id")) == ""), lit("null_measure_id")),
            when(col("ingestion_ts").isNull(), lit("null_ingestion_ts")),
        ),
    )
    .withColumn("dq_run_ts", current_timestamp())
)

cdc_clean_df = cdc_flagged_df.filter(col("dq_failed_rules") == "")
cdc_quarantine_df = cdc_flagged_df.filter(col("dq_failed_rules") != "")

(
    cdc_clean_df.drop("dq_failed_rules", "dq_run_ts")
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(SILVER_HEALTH_OUTCOMES_CLEAN_TABLE)
)

(
    cdc_quarantine_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(SILVER_HEALTH_OUTCOMES_QUARANTINE_TABLE)
)

# Compatibility output: existing silver table points to clean data
(
    cdc_clean_df.drop("dq_failed_rules", "dq_run_ts")
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(SILVER_HEALTH_OUTCOMES_TABLE)
)


# --- ACS -> Silver Socioeconomic Indicators ---
acs_bronze_df = spark.table(BRONZE_ACS_TABLE)

acs_conformed_df = (
    acs_bronze_df
    .withColumn("county_fips", lpad(trim(col("county_fips").cast("string")), 5, "0"))
    .withColumn("acs_year", col("acs_year").cast("int"))
    .withColumn("poverty_pct", col("S1701_C03_001E").cast("double"))
    .withColumn("median_household_income", col("S1901_C01_012E").cast("double"))
    .withColumn("county_label", trim(col("NAME")))
    .withColumn("state_fips", lpad(trim(col("state").cast("string")), 2, "0"))
    .withColumn("county_fips_3", lpad(trim(col("county").cast("string")), 3, "0"))
    .withColumn("source_url", col("source_url"))
    .withColumn("source_system", col("source_system"))
    .withColumn("source_path", col("source_path"))
    .withColumn("ingestion_ts", col("ingestion_ts"))
    .select(
        "county_fips",
        "acs_year",
        "county_label",
        "state_fips",
        "county_fips_3",
        "poverty_pct",
        "median_household_income",
        "source_url",
        "source_system",
        "source_path",
        "ingestion_ts",
    )
)

acs_flagged_df = (
    acs_conformed_df
    .withColumn(
        "dq_failed_rules",
        with_failed_rules(
            when((col("county_fips").isNull()) | (length(col("county_fips")) != 5), lit("invalid_county_fips")),
            when(col("poverty_pct").isNull(), lit("null_poverty_pct")),
            when((col("poverty_pct") < 0) | (col("poverty_pct") > 100), lit("poverty_pct_out_of_range_0_100")),
            when(col("median_household_income").isNull(), lit("null_median_household_income")),
            when(col("median_household_income") < 0, lit("median_household_income_negative")),
            when(col("ingestion_ts").isNull(), lit("null_ingestion_ts")),
        ),
    )
    .withColumn("dq_run_ts", current_timestamp())
)

acs_clean_df = acs_flagged_df.filter(col("dq_failed_rules") == "")
acs_quarantine_df = acs_flagged_df.filter(col("dq_failed_rules") != "")

(
    acs_clean_df.drop("dq_failed_rules", "dq_run_ts")
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(SILVER_SOCIOECONOMIC_CLEAN_TABLE)
)

(
    acs_quarantine_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(SILVER_SOCIOECONOMIC_QUARANTINE_TABLE)
)

# Compatibility output: existing silver table points to clean data
(
    acs_clean_df.drop("dq_failed_rules", "dq_run_ts")
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(SILVER_SOCIOECONOMIC_TABLE)
)


# --- DQ Monitoring (run-level metrics) ---
cdc_total = cdc_flagged_df.count()
cdc_clean = cdc_clean_df.count()
cdc_quarantine = cdc_quarantine_df.count()

acs_total = acs_flagged_df.count()
acs_clean = acs_clean_df.count()
acs_quarantine = acs_quarantine_df.count()

monitoring_rows = [
    ("silver", "health_outcomes", cdc_total, cdc_clean, cdc_quarantine),
    ("silver", "socioeconomic_indicators", acs_total, acs_clean, acs_quarantine),
]

monitoring_df = (
    spark.createDataFrame(
        monitoring_rows,
        ["layer", "dataset", "rows_total", "rows_clean", "rows_quarantine"],
    )
    .withColumn("pass_rate", when(col("rows_total") == 0, lit(0.0)).otherwise(col("rows_clean") / col("rows_total")))
    .withColumn(
        "status",
        when(col("rows_total") == 0, lit("FAIL"))
        .when(col("rows_quarantine") > 0, lit("WARN"))
        .otherwise(lit("PASS")),
    )
    .withColumn("run_ts", current_timestamp())
)

(
    monitoring_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(DQ_MONITORING_TABLE)
)

print(f"Wrote CDC clean rows: {cdc_clean} -> {SILVER_HEALTH_OUTCOMES_CLEAN_TABLE}")
print(f"Wrote CDC quarantine rows: {cdc_quarantine} -> {SILVER_HEALTH_OUTCOMES_QUARANTINE_TABLE}")
print(f"Wrote ACS clean rows: {acs_clean} -> {SILVER_SOCIOECONOMIC_CLEAN_TABLE}")
print(f"Wrote ACS quarantine rows: {acs_quarantine} -> {SILVER_SOCIOECONOMIC_QUARANTINE_TABLE}")
print(f"Appended DQ monitoring rows -> {DQ_MONITORING_TABLE}: {monitoring_df.count()}")

# Shared config for Databricks capstone pipeline scripts
# Default: managed Unity Catalog Volumes.
# To pivot to external volumes later, update volume DDL in src/00_setup_env.py
# and ensure these SOURCE_PATH values point to the external volume paths.

CATALOG = "bootcamp_students"
SCHEMA = "health_equity_capstone_jpmajesty2019"

BRONZE_CDC_PLACES_TABLE = f"{CATALOG}.{SCHEMA}.bronze_cdc_places"
BRONZE_ACS_TABLE = f"{CATALOG}.{SCHEMA}.bronze_census_acs"

SILVER_HEALTH_OUTCOMES_TABLE = f"{CATALOG}.{SCHEMA}.silver_health_outcomes"
SILVER_SOCIOECONOMIC_TABLE = f"{CATALOG}.{SCHEMA}.silver_socioeconomic_indicators"

SILVER_HEALTH_OUTCOMES_CLEAN_TABLE = f"{CATALOG}.{SCHEMA}.silver_health_outcomes_clean"
SILVER_HEALTH_OUTCOMES_QUARANTINE_TABLE = f"{CATALOG}.{SCHEMA}.silver_health_outcomes_quarantine"
SILVER_SOCIOECONOMIC_CLEAN_TABLE = f"{CATALOG}.{SCHEMA}.silver_socioeconomic_clean"
SILVER_SOCIOECONOMIC_QUARANTINE_TABLE = f"{CATALOG}.{SCHEMA}.silver_socioeconomic_quarantine"

DQ_MONITORING_TABLE = f"{CATALOG}.{SCHEMA}.dq_monitoring_runs"

GOLD_HEALTH_EQUITY_STATS_TABLE = f"{CATALOG}.{SCHEMA}.gold_health_equity_stats"
GOLD_DQ_SUMMARY_TABLE = f"{CATALOG}.{SCHEMA}.dq_gold_validation_summary"

RAW_DOCS_TABLE = f"{CATALOG}.{SCHEMA}.raw_docs"
CHUNKED_DOCS_TABLE = f"{CATALOG}.{SCHEMA}.chunked_docs"

CDC_PLACES_SOURCE_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/cdc_places/"
ACS_SOURCE_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/census_acs/"
CDC_PLACES_SOURCE_FILE="cdc_places.csv"
ACS_SOURCE_FILE="census_acs.csv"


CDC_PLACES_BULK_CSV_URL = "https://data.cdc.gov/api/views/swc5-untb/rows.csv?accessType=DOWNLOAD"

DOCS_SOURCE_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/cdc_who_docs/"

LOCKED_DOC_SOURCES = {
    "cdc_advancing_health_equity_collection.html": "https://www.cdc.gov/pcd/collections/Advancing_Health_Collection.htm",
    "cdc_mapping_chronic_disease_collection.html": "https://www.cdc.gov/pcd/collections/Mapping_Chronic_Disease.htm",
    "cdc_rural_health_disparities_2025.html": "https://www.cdc.gov/pcd/issues/2025/25_0202.htm",
    "cdc_health_equity_science_sdoh.html": "https://www.cdc.gov/health-equity-chronic-disease/hcp/health-equity-science/index.html",
    "who_world_health_statistics_2025.pdf": "https://iris.who.int/server/api/core/bitstreams/c992fbdc-11ef-43db-a478-7e7a195403ae/content",
}
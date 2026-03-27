# Shared config for Databricks capstone pipeline scripts

CATALOG = "bootcamp_students"
SCHEMA = "health_equity_capstone_jpmajesty2019"

BRONZE_CDC_PLACES_TABLE = f"{CATALOG}.{SCHEMA}.bronze_cdc_places"
BRONZE_ACS_TABLE = f"{CATALOG}.{SCHEMA}.bronze_census_acs"

CDC_PLACES_SOURCE_PATH = "dbfs:/FileStore/capstone/raw/cdc_places.csv"
ACS_SOURCE_PATH = "dbfs:/FileStore/capstone/raw/census_acs.csv"

# Shared config for Databricks capstone pipeline scripts
# Default: managed Unity Catalog Volumes.
# To pivot to external volumes later, update volume DDL in src/00_setup_env.py
# and ensure these SOURCE_PATH values point to the external volume paths.

CATALOG = "bootcamp_students"
SCHEMA = "health_equity_capstone_jpmajesty2019"

BRONZE_CDC_PLACES_TABLE = f"{CATALOG}.{SCHEMA}.bronze_cdc_places"
BRONZE_ACS_TABLE = f"{CATALOG}.{SCHEMA}.bronze_census_acs"

CDC_PLACES_SOURCE_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/cdc_places/"
ACS_SOURCE_PATH = f"/Volumes/{CATALOG}/{SCHEMA}/census_acs/"
CDC_PLACES_SOURCE_FILE="cdc_places.csv"
ACS_SOURCE_FILE="census_acs.csv"


CDC_PLACES_BULK_CSV_URL = "https://data.cdc.gov/api/views/swc5-untb/rows.csv?accessType=DOWNLOAD"
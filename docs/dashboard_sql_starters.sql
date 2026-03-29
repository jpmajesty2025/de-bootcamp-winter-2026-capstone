-- Dashboard SQL Starters (Track C: C2 + C3)
-- Date: 2026-03-29
-- POC: Capstone Student
-- TL;DR: Starter queries for KPI tiles, core visuals, and reconciliation checks
-- Source table: bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats

-- =========================================================
-- Optional parameter convention:
-- Replace 'DIABETES' below with your dashboard parameter value (e.g., OBESITY, BPHIGH)
-- =========================================================

-- C2.1 KPI TILE: Core metrics for selected measure
SELECT
  AVG(data_value) AS avg_outcome_value,
  AVG(poverty_pct) AS avg_poverty_pct,
  AVG(median_household_income) AS avg_median_household_income,
  COUNT(DISTINCT CASE WHEN health_burden_band IN ('high', 'very_high') THEN county_fips END) AS high_burden_counties
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
WHERE measure_id = 'DIABETES';
 
 -- C2.1a modified: KPI TILE: Core metrics by measure (for parameter-driven dashboard)
 SELECT
  measure_id,
  AVG(data_value) AS avg_outcome_value,
  AVG(poverty_pct) AS avg_poverty_pct,
  AVG(median_household_income) AS avg_median_household_income,
  COUNT(DISTINCT
    CASE
      WHEN health_burden_band IN ('high', 'very_high') THEN county_fips
    END
  ) AS high_burden_counties
FROM
  bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
GROUP BY
  measure_id


-- C2.1b: KPI TILE: Core metrics by measure with high burden focus (for parameter-driven dashboard)
SELECT
  measure_id,
  AVG(data_value) AS avg_outcome_value,
  AVG(
    CASE
      WHEN health_burden_band IN ('high', 'very_high') THEN poverty_pct
    END
  )
    / 100 AS avg_poverty_pct_high_burden,
  AVG(
    CASE
      WHEN health_burden_band IN ('high', 'very_high') THEN median_household_income
    END
  ) AS avg_median_income_high_burden,
  COUNT(DISTINCT
    CASE
      WHEN health_burden_band IN ('high', 'very_high') THEN county_fips
    END
  ) AS high_burden_counties
FROM
  bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
GROUP BY
  measure_id

-- C2.2 modified: VISUAL: Top 10 counties by outcome burden (filter-ready via measure_id, enforced in SQL)
WITH ranked AS (
  SELECT
    measure_id,
    state_abbr,
    county_name,
    data_value,
    ROW_NUMBER() OVER (
      PARTITION BY measure_id
      ORDER BY data_value DESC
    ) AS rn
  FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
)
SELECT
  measure_id,
  state_abbr,
  county_name,
  data_value
FROM ranked
WHERE rn <= 10
ORDER BY measure_id, data_value DESC;

-- C2.3 modified: VISUAL: Poverty vs outcome association (scatter, filter-ready via measure_id)
SELECT
  measure_id,
  county_fips,
  state_abbr,
  county_name,
  poverty_pct,
  data_value
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats;

-- C2.4 modified: VISUAL: Burden distribution by poverty band (filter-ready via measure_id)
SELECT
  measure_id,
  poverty_band,
  health_burden_band,
  COUNT(DISTINCT county_fips) AS county_count
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
GROUP BY measure_id, poverty_band, health_burden_band
ORDER BY measure_id, poverty_band, health_burden_band;

-- C2.5 VISUAL (proxy): Community income bands vs outcomes
WITH county_proxy AS (
  SELECT
    county_fips,
    state_abbr,
    county_name,
    data_value,
    median_household_income,
    poverty_pct,
    CASE
      WHEN median_household_income < 50000 THEN 'lower_income_proxy'
      WHEN median_household_income < 70000 THEN 'mid_income_proxy'
      ELSE 'higher_income_proxy'
    END AS community_income_proxy
  FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
  WHERE measure_id IN ('DIABETES', 'OBESITY', 'BPHIGH')
)
SELECT
  community_income_proxy,
  AVG(data_value) AS avg_outcome_value,
  COUNT(*) AS row_count
FROM county_proxy
GROUP BY community_income_proxy
ORDER BY community_income_proxy;

-- =========================================================
-- C3 Reconciliation checks (dashboard vs gold)
-- =========================================================

-- C3.1 Rowcount + county coverage for selected measure
SELECT
  COUNT(*) AS row_count,
  COUNT(DISTINCT county_fips) AS distinct_counties
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
WHERE measure_id = 'DIABETES';

-- C3.2 Null checks for key fields used in visuals
SELECT
  SUM(CASE WHEN data_value IS NULL THEN 1 ELSE 0 END) AS null_data_value_rows,
  SUM(CASE WHEN poverty_pct IS NULL THEN 1 ELSE 0 END) AS null_poverty_rows,
  SUM(CASE WHEN county_fips IS NULL THEN 1 ELSE 0 END) AS null_county_fips_rows
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
WHERE measure_id = 'DIABETES';

-- C3.3 Aggregate spot-check for KPI consistency
SELECT
  measure_id,
  ROUND(AVG(data_value), 4) AS avg_data_value,
  ROUND(AVG(poverty_pct), 4) AS avg_poverty_pct
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
WHERE measure_id IN ('DIABETES', 'OBESITY', 'BPHIGH')
GROUP BY measure_id
ORDER BY measure_id;

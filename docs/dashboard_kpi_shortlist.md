# Dashboard KPI & Visual Shortlist (C1)

**Date:** 2026-03-29  
**POC:** Capstone Student  
**TL;DR:** Use Gold-table-native KPIs and 4 core visuals mapped to the 3 demo questions; keep `measure_id` as a required dashboard filter to avoid mixed-metric distortion.

---

## Source Table

- `bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats`

Gold columns used:
- `county_fips`, `state_abbr`, `state_name`, `county_name`
- `measure_id`, `measure_name`, `data_value`
- `poverty_pct`, `median_household_income`
- `health_burden_band`, `poverty_band`
- `health_year`, `acs_year`

---

## KPI Tiles (Top Row)

1. **Avg Outcome Value (selected measure)**
2. **Avg Poverty %**
3. **Median Household Income (avg across joined county-measure rows)**
4. **High/Very-High Burden County Count**

> Dashboard-level required filter: `measure_id` (e.g., `DIABETES`, `OBESITY`, `BPHIGH`).

### KPI SQL (starter)

```sql
SELECT
  AVG(data_value) AS avg_outcome_value,
  AVG(poverty_pct) AS avg_poverty_pct,
  AVG(median_household_income) AS avg_median_household_income,
  COUNT(DISTINCT CASE WHEN health_burden_band IN ('high', 'very_high') THEN county_fips END) AS high_burden_counties
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
WHERE measure_id = 'DIABETES';
```

---

## Visual Shortlist (C1)

## V1) Top 10 Counties by Outcome Burden
**Type:** Horizontal bar chart  
**Demo mapping:** Q1 (worst burden counties)

```sql
SELECT
  state_abbr,
  county_name,
  data_value
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
WHERE measure_id = 'DIABETES'
ORDER BY data_value DESC
LIMIT 10;
```

## V2) Poverty % vs Outcome (Association View)
**Type:** Scatter plot (`poverty_pct` x-axis, `data_value` y-axis)  
**Demo mapping:** Q1 (social factor association)

```sql
SELECT
  county_fips,
  state_abbr,
  county_name,
  poverty_pct,
  data_value
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
WHERE measure_id = 'DIABETES';
```

## V3) Burden Distribution by Poverty Band
**Type:** Stacked bar (or heatmap matrix)  
**Demo mapping:** Q3 (community segmentation for interventions)

```sql
SELECT
  poverty_band,
  health_burden_band,
  COUNT(DISTINCT county_fips) AS county_count
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
WHERE measure_id = 'DIABETES'
GROUP BY poverty_band, health_burden_band
ORDER BY poverty_band, health_burden_band;
```

## V4) Rural Proxy Comparison (Non-CBSA fallback)
**Type:** Box/violin/bar by county-size proxy  
**Demo mapping:** Q2 (rural/urban pattern proxy until explicit rural flag is added)

```sql
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
```

---

## Dashboard Guardrails / Caveats

1. **Inner join caveat:** Gold uses `inner join` on `county_fips`; counties missing either side are excluded.
2. **Global filter required:** Always filter `measure_id` for interpretable KPIs/charts.
3. **Known cleaning follow-up:** Document chunking lane has HTML/JS boilerplate noise; this affects KA quality, not Gold dashboard metrics.
4. **Interpretation note:** Current Gold table does not include a true rural/urban classifier; use a temporary proxy visual or add RUCC/NCHS later.

---

## C2 Build Order

1. KPI tiles (with `measure_id` parameter)
2. V1 Top 10 burden counties
3. V2 Poverty vs outcome scatter
4. V3 Poverty-band vs burden matrix
5. V4 Optional proxy comparison (or replace with state-level trend if preferred)

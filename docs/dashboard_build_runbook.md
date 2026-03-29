# Dashboard Build Runbook (Track C: C2 + C3)

**Date:** 2026-03-29  
**POC:** Capstone Student  
**TL;DR:** Use the SQL starters to build 4 core dashboard visuals, enforce a `measure_id` filter, then run reconciliation checks and capture evidence.

---

## 1) Inputs

- Gold table: `bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats`
- Query pack: `docs/dashboard_sql_starters.sql`
- KPI/visual shortlist: `docs/dashboard_kpi_shortlist.md`

---

## 2) C2 Build Steps (Databricks SQL)

1. Open SQL Editor and run queries from `docs/dashboard_sql_starters.sql`.
2. Create dashboard: **Health Equity Insights (MVP)**.
3. Add visual tiles in this order:
   - KPI tile (C2.1)
   - Top 10 counties bar chart (C2.2)
   - Poverty vs outcome scatter (C2.3)
   - Burden by poverty band (C2.4)
   - Optional proxy view (C2.5)
4. Add a dashboard filter for `measure_id` and wire all widgets to it.
5. Save and verify all visuals render for at least:
   - `DIABETES`
   - `OBESITY`
   - `BPHIGH`

---

## 3) C3 Reconciliation Steps

Run C3 checks from `docs/dashboard_sql_starters.sql`:

- **C3.1** Rowcount + county coverage  
- **C3.2** Null checks (`data_value`, `poverty_pct`, `county_fips`)  
- **C3.3** Aggregate spot-check by measure (`DIABETES`, `OBESITY`, `BPHIGH`)

Acceptance:
- No major contradictions between dashboard widgets and SQL outputs.
- Null-checks should remain at expected safe levels for selected measures.
- KPI values on dashboard match SQL results for same filter state.

---

## 4) Evidence to Capture

1. Dashboard screenshot showing filter + at least 3 visuals.
2. SQL result screenshot(s) for C3 checks.
3. Short note: any caveats or interpretation constraints.

Save screenshots under `docs/` with timestamped filenames.

---

## 5) Known Caveats

- Gold is built from an `inner join` on `county_fips`; unmatched counties are excluded.
- Keep `measure_id` filtering enabled to avoid mixed-metric distortion.
- Rural/urban is currently proxy-based unless a dedicated classifier is added.

---

## 6) Definition of Done (Track C Phase)

- [ ] C2 visuals built and filterable
- [ ] C3 reconciliation checks executed
- [ ] Evidence captured in `docs/`
- [ ] Checklist/session notes updated

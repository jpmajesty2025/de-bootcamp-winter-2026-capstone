# Capstone Project Brainstorm — Winter 2026 DE Bootcamp
**Date:** 2026-02-20
**Context:** 5-week Data Engineering Bootcamp (Databricks-heavy) + Analytics Engineering Bootcamp

---

## Bootcamp Tool Stack

### DE Bootcamp
- Week 1: Data Lakes & Delta Tables
- Week 2: Databricks & Advanced Spark
- Week 3: Managing Unstructured Data
- Week 4: Structured Streaming — Kafka → Delta Live Tables
- Week 5: Building AI Agents with Databricks

### AE Bootcamp (fair game for capstone)
- Airflow (orchestration, Iceberg loading, data quality, backfilling)
- Analytical patterns (growth accounting, change data capture)
- dbt (basics + advanced)
- Snowflake advanced (VARIANT type, Cortex AI: AI_PARSE_DOCUMENT, AI_EXTRACT, AI_EMBED)

---

## Project Requirements
- Must have a **pipeline**
- **Data quality controls**
- **Documentation and visualization**
- Must be **deployed in the cloud**
- **Conceptual data model** due by end of Week 3
- *(Today: last day of Week 1)*

---

## Data Source Direction
Health-related data: CDC, WHO, and related public health APIs/datasets.

---

## 💡 Idea 1: Public Health Intelligence Platform *(Recommended — covers the most ground)*

**Core concept**: A multi-layered pipeline that ingests both **structured** (epidemiological statistics) and **unstructured** (WHO/CDC PDF reports, bulletins) health data, transforms it for analytics, and surfaces insights via an AI agent.

### Data Sources
- [CDC PLACES](https://www.cdc.gov/places/) — county-level chronic disease prevalence (diabetes, obesity, heart disease, mental health)
- [CDC Wonder API](https://wonder.cdc.gov/) — mortality/morbidity by cause of death
- [WHO Global Health Observatory API](https://www.who.int/data/gho/info/gho-odata-api) — global health indicators
- CDC/WHO PDF reports and guidelines (unstructured)

### Pipeline Architecture

```
[CDC/WHO APIs + PDFs]
        ↓
[Airflow] — orchestrates batch ingestion
        ↓
[Delta Lake / Iceberg] — raw / bronze layer
        ↓
[Spark on Databricks] — cleaning, enrichment (silver layer)
        ↓
[Delta Live Tables] — quality-checked, curated gold layer
        ↓
[dbt on Snowflake] — analytical models (growth accounting, CDC patterns)
        ↓
[Cortex AI (AI_PARSE_DOCUMENT, AI_EXTRACT)] — extract insights from PDFs
        ↓
[Databricks AI Agent] — answer natural language health questions
        ↓
[Dashboard] — Databricks SQL Dashboard or similar
```

### Why It Works
- ✅ Week 3 unstructured data (PDFs → Spark NLP / Cortex AI)
- ✅ Week 4 streaming (Kafka → Delta Live Tables for real-time WHO alerts)
- ✅ Week 5 AI agents
- ✅ Airflow orchestration + Iceberg from AE bootcamp
- ✅ dbt models + Snowflake Cortex from AE bootcamp
- ✅ Growth accounting patterns (e.g., how chronic disease rates change YoY across counties)
- ✅ Data quality via Delta Live Table expectations + dbt tests

---

## 💡 Idea 2: Chronic Disease & Social Determinants Correlator *(Focused, analytically rich)*

**Core concept**: Correlate CDC chronic disease data (PLACES dataset) with social determinants of health (income, education, food access) to identify high-risk communities. Heavy analytics engineering focus.

### What Makes It Interesting
- CDC PLACES has 36 health measures across 27,000+ US census tracts — great for spatial analytics
- Join with Census Bureau data (ACS) for socioeconomic variables
- Use **change data capture** patterns (from AE bootcamp) to track how county-level metrics shift over annual releases
- **Growth accounting** to measure which conditions are worsening fastest in which regions
- dbt for all transformation logic
- Snowflake Cortex `AI_EMBED` to create semantic search over health measure descriptions

### Streaming Angle
Simulate a streaming layer with Kafka publishing new "data release" events triggering pipeline refreshes via Delta Live Tables.

---

## 💡 Idea 3: Vaccine Coverage vs. Disease Outbreak Tracker *(Streaming-forward)*

**Core concept**: Real-time pipeline tracking vaccine coverage rates against disease incidence, with anomaly detection.

### Data Sources
- CDC vaccine coverage data (NIS — National Immunization Survey)
- CDC disease incidence data (Wonder API)
- WHO immunization data (GHO API)

### Streaming Angle
- Kafka topics simulating incoming health surveillance reports (state-level weekly disease counts)
- Delta Live Tables consuming the stream, applying quality expectations
- Databricks AI agent detects statistical anomalies (e.g., measles uptick in low-vaccination counties)

**Best fit if**: You want the streaming/Kafka components to be front-and-center.

---

## 💡 Idea 4: Health Document RAG Pipeline *(AI/unstructured-forward)*

**Core concept**: Ingest CDC/WHO clinical guidelines, policy documents, and research summaries → build a retrieval-augmented generation (RAG) system for querying public health knowledge.

- Spark handles large-scale PDF extraction (Week 3)
- Snowflake Cortex `AI_PARSE_DOCUMENT` + `AI_EMBED` for embeddings
- Databricks AI agent (Week 5) answers questions like *"What does the CDC recommend for pre-diabetes screening in adults over 45?"*
- Delta Lake stores document metadata + embedding vectors
- Airflow orchestrates nightly ingestion of new CDC/WHO publications

**Best fit if**: You're interested in the AI/LLM engineering side of things.

---

## 🧭 Recommendation

**Idea 1** gives the best coverage of tools from both bootcamps and would make the strongest portfolio piece. **Idea 2** may be more tractable timeline-wise for a cleaner scope.

### Open Questions to Narrow Down
1. **Streaming vs. AI/unstructured emphasis?** (Week 4 vs. Week 5 focus)
2. **Existing cloud accounts?** (Snowflake + Databricks workspace already set up?)
3. **US-only or global datasets?**
4. **Specific health topic preference?** (chronic disease, infectious disease, mental health, maternal health, etc.)

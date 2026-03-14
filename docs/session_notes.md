# Capstone Project Session Notes
**Project:** Winter 2026 DE Bootcamp Capstone
**Last Updated:** 2026-03-13

---

## Purpose
Running log of decisions, answers to clarifying questions, and next steps. Updated each session to survive context resets.

---

## Project Background
- **Bootcamp:** 5-week Data Engineering Bootcamp (Databricks-heavy) + Analytics Engineering Bootcamp
- **Timeline:** Today is Week 1, last day (as of ~2026-02-20 brainstorm session)
- **Requirements:** Pipeline, data quality controls, documentation/visualization, deployed in cloud, conceptual data model due end of Week 3

## Theme
Health-related data: CDC, WHO, and related public health APIs/datasets.

## Candidate Ideas (from brainstorm doc)
1. **Public Health Intelligence Platform** — multi-layered pipeline, structured + unstructured, AI agent *(recommended)*
2. **Chronic Disease & Social Determinants Correlator** — CDC PLACES + Census ACS, analytics-heavy *(more tractable)*
3. **Vaccine Coverage vs. Disease Outbreak Tracker** — streaming-forward, Kafka-centric
4. **Health Document RAG Pipeline** — AI/unstructured-forward, Cortex AI + Databricks agent

---

## Clarifying Questions & Decisions
*(5 hypothesized questions from lost session — awaiting user confirmation)*

- [x] Q1: **Platform confirmed: Databricks workspace (bootcamp-provided) + S3 cloud storage.** Stack is Databricks-native (Delta Lake on S3). Snowflake not required (AE bootcamp tools optional).
- [x] Q2: **Scope of pipeline.** Expand beyond unstructured CDC docs. Two confirmed sources: CDC PLACES (structured, county-level chronic disease metrics) + CDC/WHO PDFs (unstructured). Both Vector RAG and Graph RAG included. User has Neo4j Academy background — graph layer is a key differentiator.
- [x] Q3: **Frontend / Visualization.** *(Discussed 2026-03-14, PDT)* Capstone requires a visualization (per Zach Wilson). 

  **Decision: Keep VitalDocs AI and the DE capstone pipeline decoupled.** Focus capstone effort on building a robust Databricks DE workflow. VitalDocs AI appears in the demo as narrative context — "the future product this pipeline will power" — not as a capstone deliverable.

  **Visualization options considered:**
  - **Option A (chosen for capstone):** Databricks SQL Dashboard — native, zero extra infra, directly queries gold Delta tables. The capstone visualization deliverable.
  - **Option B (product roadmap):** Add `/analytics` route to VitalDocs AI — pulls from Databricks SQL REST API, embedded charts/maps. More cohesive product but additive scope post-capstone.
  - **Option C:** Streamlit on Databricks — more interactive than SQL Dashboard, still no extra infra.
  - **Option D:** External BI (Tableau, Power BI) — overkill, adds infra complexity for no capstone credit.

  **Light pointer:** A link/button in VitalDocs AI pointing to the Databricks SQL Dashboard is ~10 min of work and tells a great demo story. ✅ Include this.

  **Backend swap (Supabase pgvector → Databricks Vector Search) is explicitly OUT of capstone scope.** That is a post-capstone product evolution. Supabase/OpenAI chat backend stays as-is for now.

  **Product vision (post-capstone):** Combined Chat + Analytics SaaS is a valid and forward-looking product direction (consistent with Databricks Genie, Tableau Pulse, Snowflake Cortex Analyst positioning). VitalDocs AI evolution: (1) `/analytics` route added, (2) chat backend swapped to Databricks Model Serving. Design system ("Clinical SaaS" aesthetic) requires no changes. Navigation: add "Search" + "Analytics" tabs.

  Sub-questions answered *(2026-03-14)*:
  - (a) **Post-capstone plans:** User is actively job-seeking (laid off ~1 year). Continuing to build VitalDocs AI is career-relevant. Backend swap (Supabase → Databricks) is a meaningful post-capstone milestone.
  - (b) **Review format:** AI auto-grader first, then human review by TAs and/or Zach Wilson.
  - (c) **Data strategy / health topic:** See Data Strategy section below.

---

## Data Strategy *(2026-03-14)*

The capstone pipeline has two outputs: (1) **Analytics dashboard** — structured data visualized; (2) **RAG agent** — NL Q&A over documents. Structured data and unstructured docs must tell the same health story.

**Three options considered:**

| Option | Structured Data | Unstructured Docs | Story |
|---|---|---|---|
| A) Chronic Disease | CDC PLACES (county-level: diabetes, obesity, heart disease, mental health) | CDC chronic disease guidelines + WHO prevention reports | "Where are Americans sickest, and what do guidelines recommend?" |
| B) Infectious Disease | CDC NIS (vaccine coverage) + CDC Wonder API (disease incidence) | CDC/WHO immunization guidelines, outbreak reports | Closest to VitalDocs AI original focus |
| C) Health Equity *(recommended)* | CDC PLACES + Census ACS (income, education, food access by county) | CDC health equity reports, WHO social determinants docs | "Which communities face worst health outcomes, and why?" |

**Option C recommended** — most analytically rich, strongest joins story (CDC PLACES + Census ACS = two clean structured sources), most visually compelling dashboard, resonates with hiring audience.

**VitalDocs AI tie-in with Option C:** Architectural, not thematic. VitalDocs AI's value is the pattern ("NL questions over health docs → cited answers"), not the specific topic. Story: *"Vibe Coding bootcamp → VitalDocs AI MVP in 48hrs using off-the-shelf components. DE capstone → production data platform powering same product vision: medallion pipeline, structured analytics, graph RAG, LLMOps."* Topic shift from infectious disease to health equity is a non-issue in this framing.

**Decision: Option C confirmed. *(2026-03-14)***

---

## Out-of-Scope Query Handling *(2026-03-14)*

**Context:** VitalDocs AI currently fails gracefully (low retrieval confidence) on topics outside its corpus. This is the product motivation for the DE capstone. A richer handling strategy was discussed — likely MVP++ tier or post-capstone, since MVP++ has plenty of DE workflow work without touching VitalDocs AI. Still a compelling demo story regardless of current VitalDocs AI behavior.

**Actions identified when a user asks an out-of-scope question:**

| Action | Value | Tier |
|---|---|---|
| Log query + user + timestamp to `failed_queries` table | Corpus gap analysis | MVP+ |
| Auto-classify query into health topic taxonomy (LLM call) | Structured demand signals, not just raw text | MVP+ |
| Track query frequency by topic cluster | High-demand topics bubble up automatically | MVP+ |
| Track per-user query history | Personalization, user-level demand signals | MVP+ |
| Return "notify me" CTA — user opts in for alerts when topic available | Demand validation + retention | MVP+ |
| Feed `failed_queries` back into Databricks pipeline as corpus expansion signal | Closes the loop — user demand drives ingestion | MVP++ |
| Admin dashboard showing top unmet topics | Product/operator visibility | MVP++ |
| A/B test graceful degradation messages | Optimize "notify me" CTA conversion | MVP++ |

**The closed loop (MVP++):** VitalDocs AI failures → `failed_queries` table → Databricks pipeline prioritization → new gold data → expanded RAG corpus → VitalDocs AI answers those questions. A genuine product feedback loop.

**VitalDocs AI changes required (when pursued):**
1. Expose retrieval confidence score; add threshold check for out-of-scope detection
2. API route: write to `failed_queries` table (Supabase now, Databricks REST API post-capstone)
3. Response logic: graceful degradation message + optional "notify me" button
4. New Supabase table: `failed_queries` (query_text, user_id, timestamp, auto_classified_topic, confidence_score)

**Capstone scope ruling:** MVP++ or post-capstone. DE workflow itself has sufficient depth to fulfill MVP++ without touching VitalDocs AI. Demo story works regardless of current VitalDocs AI out-of-scope behavior.



**Product motivation framing (locked):** The thematic disconnect between VitalDocs AI's current corpus (infectious disease/immunization) and Option C (chronic disease + health equity) is not a weakness — it's the product narrative. Current VitalDocs AI gracefully fails on out-of-scope questions (e.g., diabetes management, county health outcomes). The DE capstone is the infrastructure that closes that gap. Demo moment: show VitalDocs AI failing on a chronic disease question today → show the capstone pipeline answering it.

> *"VitalDocs AI launched with a narrow corpus. Real users immediately asked questions it couldn't answer. The DE capstone builds the data infrastructure that closes that gap — medallion pipeline, CDC PLACES + Census ACS structured data, broadened document corpus, graph-enriched retrieval, production-grade RAG agent. Same product vision, dramatically expanded scope."*
- [x] Q4: **Streaming.** *(Decided 2026-03-14)* **Not included — no legitimate business case.** CDC PLACES, Census ACS, and CDC/WHO PDFs all publish on annual/periodic cycles with no sub-hour latency requirements. Batch ingestion (Airflow/scheduled Databricks jobs) is the correct pattern. Streaming is not a capstone requirement. Simulating Kafka just to check a box would be the wrong call. Proposal will include explicit rationale: *"Streaming evaluated and ruled out — data sources publish periodically with no sub-hour latency requirements. Batch ingestion is the appropriate pattern."* Demonstrates stronger engineering judgment than a forced streaming implementation.
- [x] Q5: **Timeline.** *(Decided 2026-03-14)* Week 5 begins 2026-03-16. No official due date listed yet — based on prior bootcamp experience, likely 2026-03-29 11:59pm (week after classes end), possibly 2026-03-22 11:59pm if earlier. **Working assumption: target MNVP by 2026-03-22 (hard internal deadline), full MVP by 2026-03-29.** Week 5 covers AI agent components — designing around them is fully justified given Week 5 starts in 2 days.

---

## Reconstructed Plan (from prior lost session + 3/14 reconstruction)
- Direction confirmed: **use VitalDocs AI MVP as jumping-off point** for DE capstone
- 3-tier plan fully reconstructed below

---

## 3-Tier Capstone Plan

### MNVP — Vector RAG + Medallion Pipeline
- Ingest CDC PLACES (structured) + CDC/WHO PDFs (unstructured) → bronze/silver/gold on Delta Lake/S3
- Vector embeddings of PDF chunks → Databricks Vector Search
- Basic Databricks AI agent: natural language → vector retrieval → cited answers
- Joins requirement met: CDC PLACES county metrics + WHO document context joined at query time
- **LLMOps (MNVP):** MLflow experiment tracking — log prompt templates, chunk size, embedding model, top-k, latency as artifacts/metrics; **Prompt Registry** (MLflow 2.4+) for versioned prompt management; **Unity Catalog** from day one — register vector indexes, models, and gold tables as governed assets; **`mlflow.evaluate()`** for hallucination detection and RAG quality scoring

### MVP+ — Graph RAG Layer (Neo4j)
- Entity extraction from ingested documents: diseases, conditions, risk factors, interventions, geographic entities, medications
- Knowledge graph in **Neo4j Aura** (hosted, accessible from Databricks)
  - Nodes: Disease, Condition, RiskFactor, Intervention, County, Document
  - Relationships: `ASSOCIATED_WITH`, `INCREASES_RISK_OF`, `RECOMMENDED_FOR`, `LOCATED_IN`, `CITED_BY`
- Upgraded agent: queries both vector index AND graph (graph for multi-hop, vector for semantic)
- Example power query: *"Which counties have high diabetes prevalence AND low fruit/vegetable access, and what do CDC guidelines recommend?"*
- **LLMOps (MVP+):** `mlflow.evaluate()` for hallucination detection, relevance, faithfulness, completeness scoring; retrieval quality metrics (precision@k, context recall); compare vector-only vs graph+vector as MLflow experiments; **AI Gateway** — centralized access control, rate limiting, and cost tracking for external model endpoints (OpenAI/Anthropic)

### MVP++ — Hybrid RAG + Streaming + Production LLMOps
- **Hybrid retrieval**: dynamic routing — graph-first for relational/multi-hop, vector-first for semantic, fused for complex queries
- **Streaming layer**: Kafka → Delta Live Tables for simulated real-time health surveillance events (new incidence reports trigger graph/pipeline updates)
- **Agentic reasoning loop**: agent autonomously chooses graph traversal, vector search, structured gold table query, or combination
- **Dashboard**: Databricks SQL + Neo4j Bloom graph visualization
- **LLMOps (MVP++):** Monitoring dashboard (latency, token cost, hallucination rate, retrieval relevance trends); A/B testing of retrieval strategies; automated quality alerts if relevance drops; streaming events → pipeline reruns → LLMOps monitors impact of new data on answer quality; **Databricks Model Serving** — serverless GPU hosting for custom embedding or fine-tuned models; **Databricks Asset Bundles (DABs)** — infrastructure-as-code for full pipeline deployment (dev → staging → production); **CI/CD via Databricks Git folders + MLOps Stacks** — automated environment promotion for pipeline and agent changes

---

## How Capstone Requirements Are Met

| Requirement | How It's Met |
|---|---|
| Pipeline | Bronze→Silver→Gold medallion + entity extraction pipeline |
| Two+ data sources with joins | CDC PLACES (structured) + WHO/CDC PDFs (unstructured) — joined via graph and at query time |
| Data quality controls | Delta Live Table expectations |
| Agentic action | Hybrid RAG agent with graph + vector + structured retrieval |
| Cloud deployed | Databricks on S3 + Neo4j Aura |
| Weeks 3–5 coverage | Unstructured (Wk3) + Streaming (Wk4) + AI Agent (Wk5) |
| LLMOps | MLflow throughout all tiers — experiment tracking → evaluation → production monitoring |

---

## Proposal Sections Required (per TA)
1. Project Description / Scope
2. Conceptual Data Model & Diagram
3. Tools, Data Sources and Formats
4. Ingestion Strategy, Data Quality Checks
5. Success Metrics, Stakeholder Value

## Capstone Technical Requirements
- One or more pipelines
- Data quality controls
- Deployed and running in the cloud
- Must have agentic action(s)
- At least two data inputs with meaningful joins, aggregations, gold-standard output (medallion architecture)

---

## Open Items
- [ ] User to confirm/correct the 5 clarifying questions and their answers
- [ ] Reconstruct 3-tier MNVP/MVP+/MVP++ plan
- [ ] Draft capstone proposal: `docs/de_capstone_proposal_draft_1.md`

---

## Session Log
| Date | Summary |
|------|---------|
| ~2026-02-20 | Initial brainstorm — 4 ideas generated, saved to `docs/winter_2026_de_bootcamp_capstone_brainstorm_1.md` |
| ~2026-02-22 | Vibe Coding bootcamp brainstorm → VitalDocs AI proposal created (`PROPOSAL.md`) |
| 2026-03-13 AM | Multi-hour session: reviewed all docs, developed 3-tier plan, was about to draft proposal — lost to API timeout |
| 2026-03-13 PM | Session recovery. Read all available docs. Reconstructed context. Identified 5 missing clarifying Q&A. User confirmed: update session notes after every exchange. |

### Clarifying Questions Before We Draft the Proposal.

1. 
Databricks workspace: Do you have an active workspace already set up from the bootcamp? And is cloud storage S3, ADLS, or DBFS?
2. 
Scope of "pipeline": Should the capstone pipeline ingest only CDC documents (like VitalDocs AI today), or expand to include structured epidemiological data too (CDC PLACES, Wonder API)? The structured data angle would add a nice analytics layer but also adds scope.
3. 
Frontend: Does the capstone need a user-facing UI, or is the Databricks SQL Dashboard / Model Serving endpoint sufficient? (VitalDocs AI's Next.js front-end could remain as-is and just point to the new Databricks backend.)
4. 
Streaming requirement: Is Kafka/streaming a required component of the capstone, or just strongly recommended? This affects whether we build a real streaming ingestion path or simulate it.
5. 
Timeline: When is the capstone due, and when does Week 5 start? That affects how much we design around the Week 5 AI agent components.
The high-confidence answer to your core question: Yes, VitalDocs AI is an excellent genesis for this capstone. The use case is already validated, 
the frontend exists, and the gap between what's built and what the bootcamp teaches is almost perfectly sized for a capstone project. 🚀
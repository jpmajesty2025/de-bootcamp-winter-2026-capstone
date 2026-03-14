### 3/13/2026
## How we got here

- Initially, I presented AdaL with ./docs/winter_2026_de_bootcamp_capstone_brainstorm_1.md. It is worth it to start here by reviewing this document. It is the result of a prior brainstorming session with Claude to develop ideas for my current Data Engineering bootcamp capstone project. I presented this document to AdaL because I was doing a separate hackathon Vibe Coding Bootcamp, put on by Zach Wilson (who runs the DE bootcamp) and Li Yin, creator of AdaL.

- The resulting brainstorming session between AdaL and I was  ./docs/saas-vibe-coding-project-brainstorm-1.md. 

- From there, we produced ./PROPOSAL.md, the proposal for Vitaldocs AI, my Vibe Coding bootcamp project. For further context, see ./submission/vitaldocs-ai.zip which is the core required files I zipped and submitted for that project. 

Note: All of this happened some weeks prior to 3/13/2026. 

Where are we now? Time to move forward with a DE bootcamp capstone. And the first step is to develop a proposal that fulfills capstone requirements. 

But we're *not* going to work from winter_2026_de_bootcamp_capstone_brainstorm_1.md. 

Instead: if possible, use the VitalDocs AI MVP we built as a jumping off point.

However, you first need to know a few things. 

What does a project proposal contain? As per one of the DE bootcamp TAs, here is the minimum a project proposal should contain:

- Project Description/Scope
- Conceptual Data Model & Diagram
- Tools, Data Sources and Formats
- Ingestion Strategy, Data Quality Checks
- Success Metrics, Stakeholder value

What does a successful capstone project itself need to have? At a minimum, this:

- one or more pipelines
- data quality controls
- must be deployed and running in the cloud
- must have some agentic action(s)
- data model must have at least two inputs so that data can be joined somewhere in the process. In other words, not ok to just scrape data from one API, clean it, dump it in a single table and call it a day. That is not sufficient. Going from raw data to production-grade data for end-users should involve meaningful joins, aggregations and other typical advanced SQL operations to prepare 'gold' standard data (if we're thinking in roughly medallion architecture terms).

What concepts and tools from DE are covered in this particular bootcamp? Perhaps the one biggest thing to note is that this bootcamp is taught using Databricks. So that will be our data platform. Additionally, as ./docs/winter_2026_de_bootcamp_capstone_brainstorm_1.md notes, any concepts or tools from my prior Analytics Engineering bootcamp are fair game to include, if they make sense, e.g. analytical patterns or dbt. But to be clear: this DE bootcamp does not assume any of the tools or concepts from the AE bootcamp. The AE and DE bootcamps are independent entities. 

The DE bootcamp is 5 weeks of classes, 2 lectures and 2 labs per week. We have completed weeks 1-4 so far. For each lecture, there is a pdf document. The lecture pdfs can be found at:

- C:\Users\llp_y\OneDrive\Documents\DataExpert.io\DE_Bootcamp_Feb_Mar_2026

Feel free to examine those as needed. 

For each lab there is a repo which is pulled into Databricks from Github and executed. I also cloned each repo to my laptop. See 

- ./de_bootcamp_lab_repos.md 

to learn where all the repos are located locally. As week 5 lectures and labs become available, I will add in that information to this documentation.

So all of the above will give you a sense where we are starting. Indeed, earlier today I presented to AdaL all of the above info and asked if it was feasible to use the VitalDocs AI as a jumping off point for the DE bootcamp capstone. We had a multi-turn conversation with a lot of back and forth and many good ideas. We developed a 3-tier plan for a MNVP, MVP+ and MVP++. At a certain point, we had completed that conversation and AdaL was ready to create a first draft of a capstone proposal. I instructed AdaL to create and save the proposal but some internal error occured, possibly upstream of AdaL. Suddenly, all of my inputs to AdaL timed out and I was forced to quit my session and reauthenticate. Because I had not instructed AdaL to save any session notes from our conversation, much of our work was lost. I did copy some items from the cli workspace and I have included them in a separate document ./adal_output_saved_from_prior_planning.md. It may be a bit disjointed but it will probably offer some additional context. Once you examine all the prior documents I referenced above and have a handle on what we need to do, please peruse this additional info in ./adal_output_saved_from_prior_planning.md. Then let me know what other information you need to fill in the blanks.







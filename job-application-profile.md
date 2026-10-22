# Job Application Profile — Atharva Mohite

Machine-readable profile for browser agents filling out job applications on my behalf.
Source of truth: `public/resume.pdf` in this repo (built from `resume/resume.tex`). If a form asks for something not
listed here, see "Rules for the agent" at the bottom. Do not invent an answer.

---

## Rules for the agent

1. Never fabricate. Every number, date, title, and tool below is verified. If a field needs a
   fact that is not in this file, stop and ask the human. Do not guess employment dates,
   salary, GPA conversions, authorization status, references, or availability.
2. Fields marked `ASK HUMAN` must be confirmed before submitting the application.
3. Prefer the exact wording in this file over paraphrasing. Bullets can be trimmed to fit a
   character limit, but do not rewrite the claims.
4. Upload `resume/Atharva Mohite Resume.pdf` (run `make` in `resume/` if it is missing) whenever a resume upload is offered, even if the form
   also parses fields.
5. Do not check "yes" on any question about prior employment with the company, referrals, or
   non-competes without asking. The EEO questions below are already answered; fill those in
   directly.
6. If a form requires a cover letter, use the blurb below as the base and adapt the last
   paragraph to the specific role. Show the draft before submitting.
7. Before hitting submit, report: company, role, URL, and any field you had to guess.
8. Automatically acknowledge applicant privacy notices when a form requires confirmation that
   the notice has been read and understood.

---

## Identity and contact

| Field | Value |
|---|---|
| Full name | Atharva Mohite |
| First / last name | Atharva / Mohite |
| Preferred name | Atharva |
| Pronouns | he/him |
| Email | amohite8@gatech.edu |
| Phone | +1 (404) 390-5358 |
| Phone country | United States (+1) |
| Current location | Atlanta, GA, USA |
| Permanent address | 699 Spring St NW, Atlanta, GA 30308, United States |
| Website | https://moriowen.github.io |
| LinkedIn | https://www.linkedin.com/in/atharva-mohite/ |
| GitHub | https://github.com/moriowen |
| Google Scholar | https://scholar.google.com/citations?hl=en&user=wMiMf_wAAAAJ |

### Work authorization

Use these answers directly. Do not ask for reconfirmation.

- Authorized to work in the US without sponsorship: Yes
- Will now or in the future require visa sponsorship: Yes
- Current visa status: F1
- Authorized to work in other countries (UK, EU, Canada, India): india and US only

These questions are legally binding on the application. Never answer them from inference.

### Demographic / EEO questions

Answer these as stated. No need to ask.

| Question | Answer |
|---|---|
| Gender | Male |
| Race / ethnicity | Asian |
| Protected veteran status | No, not a protected veteran |
| Disability status | No, I do not have a disability |
| Hispanic or Latino | No |

If a form words one of these differently (for example, a self-identification form with a
"Yes / No / I don't wish to answer" set), pick the option matching the answers above. Decline to
self-identify only if none of the options fits.

---

## Summary / "Tell us about yourself"

Software engineer, close to four years at JPMorgan Chase on distributed trade settlement
systems, now doing an MS in Computer Science at Georgia Tech on the machine learning track.
The work has been half backend systems at scale (Kafka, Spring WebFlux, Elasticsearch,
Kubernetes) and, more recently, LLM agent tooling: an agentic SDLC pipeline and an agent-driven
regression framework that 30+ engineers use. Two IEEE papers on video understanding and
computer vision.

Short version (under 300 characters):

> Software engineer, ~4 years at JPMorgan Chase building distributed trade settlement systems,
> currently an MS CS (ML) student at Georgia Tech. Recent work is LLM agents applied to the
> software development lifecycle: agentic PR generation and an agent-built regression framework.

---

## Education

### Georgia Institute of Technology — Aug 2026 to May 2028 (expected)
- Degree: Master of Science, Computer Science (specialization: Machine Learning)
- Location: Atlanta, GA, USA
- Coursework: Machine Learning, Big Data Systems, Data Visualization and Analytics
- GPA: 4.0

### University of Mumbai — Aug 2019 to May 2023
- Degree: Bachelor of Technology (B.Tech.), Computer Science
- Location: Mumbai, India
- CGPA: 9.39 / 10
- If a form demands a 4.0-scale GPA: 3.9

---

## Work experience

All three entries are the same employer: **JPMorgan Chase**. Some forms want one entry with
promotions; others want three. Use whichever the form supports.

### Software Engineer II — JPMorgan Chase — Jan 2026 to Aug 2026
Location: Mumbai, India (confirm office city before entering)

- Owned cross-service design and production readiness for a new business line across 7
  microservices on a multi-tenant settlement platform, scaling throughput to 5M+ trades per day.
- Built an agentic SDLC pipeline that autonomously translated Jira requirements into code
  changes across a multi-service architecture, reproduced issues with local infrastructure,
  validated via automated tests, and raised developer-ready PRs for review, with 75% of PRs
  merged with minimal edits.
- Built a regression framework using LLM agents that generates and diagnoses multi-service test
  workflows, automating 300+ scenarios and cutting manual test effort by 90%; adopted by 30+
  engineers across 5 teams.
- Designed an aggregation engine in Spring Boot reducing high-volume trade streams into
  consolidated settlement instructions across configurable dimensions, cutting instruction
  volume by 70%.

### Software Engineer I — JPMorgan Chase — Feb 2023 to Dec 2025
Location: Mumbai, India 

- Led extraction of a high-throughput microservice from a legacy trade settlement monolith,
  processing 1M+ messages per day, with an event-driven, non-blocking stack using Kafka and
  Spring WebFlux.
- Designed distributed end-of-day orchestration coordinating 3 services to close and settle the
  day's book within a 30-minute cutoff, handling race conditions, ordering dependencies, and
  concurrent state transitions with idempotent replay on failure.
- Architected a materialized datastore using Elasticsearch, aggregating and rehydrating data
  from multiple source systems to provide sub-150ms complex search over 750k records, enabling
  the decommission of 4 legacy systems.
- Migrated 15 legacy applications to an in-house Kubernetes platform, saving $450k annually in
  infrastructure costs and reducing deployment time by 50%.

### Software Engineer Intern — JPMorgan Chase — Jan 2022 to Jul 2022
Location:  Bengaluru, India 

- Developed a cloud resource discovery framework that discovered 10k+ resources, consolidating
  AWS Config, Splunk, Terraform, and tagging APIs into a unified inventory with Qlik Sense
  dashboards for tracking resource ownership, enabling data-driven cleanup decisions and
  improving infrastructure visibility for the DevOps team.

### Employment-form details
- Reason for leaving each role: Education
- Salary / compensation (current, past, or expected): 100k+ for FTE or 50$+ per hour
- May we contact this employer: Yes

---

## Skills (use these exact terms for skill checkboxes and keyword fields)

- **Languages:** Python, Java, TypeScript, SQL
- **AI/ML:** LLM agents, RAG, LangChain, LangGraph, MCP, vector databases, scikit-learn,
  pandas, evals and prompt design
- **Backend & infra:** Spring Boot, Flask, Node.js, Django, relational databases (Oracle),
  Elasticsearch, AWS, Terraform, Kubernetes, Docker, Jenkins, shell scripting, React, Next.js
- **Other:** system design (scalable and distributed systems), event-driven architecture
  (Kafka), RESTful and GraphQL API design, cloud architecture, testing (unit, integration,
  E2E), CI/CD pipelines, design patterns, monitoring and observability (Splunk, Grafana)

Do not claim a technology that is not on this list. If a form asks for years of experience in
a specific tool and it is not derivable from the dates above, 4 years in all cases. 

---

## Projects

### Splice — PyTorch, Transformers, vLLM
- Cut time to first token 1.7× and raised throughput 52% at 90% memory reuse, and up to 2.3× with
  all memories precached, by re-rotating stored KV through vLLM's KV connector API without engine
  changes.
- Showed uncorrected reuse halves answer quality and the best of 3 published fixes needs ~70%
  recompute to recover it, by benchmarking them with Mistral-7B on 1,986 LoCoMo questions.
- Link: https://moriowen.github.io/projects/splice/

### Canary — PyTorch, LightGBM, vLLM
- Cut agent compute 46% at a 2% loss of successful runs, nearly double the best fixed turn limit,
  by stopping likely failures early.
- Showed most early failure signal is task difficulty, AUROC 0.70 across all runs vs. 0.54 between
  attempts at the same issue, by training LightGBM and GRU monitors on 147k SWE-agent and
  OpenHands trajectories.
- Link: https://moriowen.github.io/projects/canary/

---

## Publications

### Leveraging LLMs for Video Querying — 2023
IEEE 7th International Conference on Computer Applications in Electrical Engineering-Recent
Advances (CERA)
- Built a long-video search pipeline converting surveillance footage into time-stamped captions
  with BMT and Vid2Seq, then used GPT-3.5, GPT-4, and LLaMA to retrieve events from
  natural-language queries.
- Benchmarked 12 action-recognition and keyframe-extraction combinations; the best result
  reached 84.53% average accuracy, and keyframe selection reduced reported per-epoch time by up
  to 68.75%.

### SecurePark — a vehicle intrusion detection system — 2022
IEEE Asian Conference on Innovation in Technology (ASIANCON)
- Trained a YOLOv5s license-plate detector on labeled training images and integrated OCR,
  vehicle authorization, alerts, saved recordings, and usage analytics into a working
  monitoring dashboard.

Paper URLs: on Google Scholar (link above). ASK HUMAN if a form needs a direct DOI.

---

## Job search preferences — ASK HUMAN to fill in and keep current

- Target roles: SWE, Data Engineer, AI Engineer, Machine Learning Engineer, Inference Engineer
- Desired start date / availability: For Summer intern - May 1 2027, for full time roles - May 30 2028
- Full-time / internship / co-op: currently looking for summer intern 
- Remote, hybrid, or onsite: anything works 
- Willing to relocate: Yes
- Geographic preferences: 
- Salary expectations: 100k+ for FTE or 50$+ per hour
- Security clearance: none
- How did you hear about us: LinkedIn
- Referral: ASK HUMAN

---

## Cover letter base

Adapt the closing paragraph per role. Show the draft to the human before submitting.

> I'm applying for [ROLE] at [COMPANY]. I spent close to four years at JPMorgan Chase on trade
> settlement infrastructure: pulling a high-throughput service out of a monolith onto Kafka and
> Spring WebFlux, building end-of-day orchestration across three services under a 30-minute
> cutoff, and cutting search over 750k records to under 150ms with Elasticsearch.
>
> Lately the work has been LLM agents pointed at our own development process. One pipeline takes
> a Jira ticket, reproduces the issue locally, writes and tests the change, and opens a PR; 75%
> of those merge with minimal edits. Another is an agent-built regression framework covering 300+
> scenarios that 30+ engineers across 5 teams now use. I'm doing an MS in Computer Science at
> Georgia Tech on the machine learning track to go deeper on the modeling side of that.
>
> [ROLE-SPECIFIC PARAGRAPH: why this company, what in the JD maps to the above.]
>
> Resume, papers, and project writeups are at moriowen.github.io. Happy to talk whenever suits.
>
> Atharva Mohite

---

## Common free-text answers

**"Why are you interested in this role?"** Role-specific. ASK HUMAN, or draft and confirm.

**"Describe a technical challenge you solved."**
> End-of-day settlement at JPMorgan had to close the day's book across three services inside a
> 30-minute cutoff. The hard part was not throughput, it was ordering: concurrent state
> transitions, race conditions between services, and the requirement that any failure be
> replayable without double-settling. I designed the orchestration around idempotent steps, so a
> retry after partial failure converges to the same state instead of compounding the problem.

**"What are you working on now?"**
> Two research projects. Canary watches a coding agent while it works and stops runs that are
> heading for failure; on held-out SWE-agent runs it cuts compute 46% while losing 2% of the runs
> that would have succeeded, nearly double what the best fixed turn limit saves. Splice reuses an
> agent's memory KV cache wherever a memory lands in the prompt. Through vLLM it cut time to first
> token 1.7× at 90% memory reuse, but uncorrected reuse halves answer quality, and fixing that
> cheaply is the open problem.

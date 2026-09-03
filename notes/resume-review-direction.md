# Resume review direction

## Goal

Update Atharva's J.P. Morgan Chase experience for senior software engineering and AI-engineering-adjacent roles. Every claim must be specific, accurate, and defensible in an interview.

## Target structure

J.P. Morgan Chase should have eight bullets:

- Software Engineer II, January 2026 to August 2026: 4 bullets
- Software Engineer I, February 2023 to December 2025: 4 bullets

Each bullet should:

- Start with a strong action verb.
- Follow an Action + Context + Result or X-Y-Z structure.
- Describe the technical implementation in concrete terms.
- Include a measurable result or scale when a verified number is available.
- Stay within one or two resume lines.
- Emphasize relevant technologies without making the sentence harder to read.

Use generally understandable descriptions when internal JPMC terminology would obscure the work. Do not invent metrics, imply projected capacity was achieved in production, or overstate AI work.

## Platform context

AME stands for Asset Movement Engine. It is a shared, distributed settlement platform made up of several services, including:

- DS, or Determine Settlements
- Matching Service
- IGS, or Instruction Gateway Service
- OSM, or Open Settlement Manifest
- RT/ARS real-time service
- Union datastore
- End-to-end regression automation framework

ICB was Atharva's line of business. Nutmeg used AME as its primary settlement engine. Atharva was one of the lead functional developers for the ICB and Nutmeg flows across these shared services. His changes had to support the new flow without breaking existing lines of business.

AME was moving from legacy VSI infrastructure to JPMC's Kubernetes platform, GKP. Atharva helped productionize the ICB flows and worked on the first GKP rollout.

The upcoming flow was designed for roughly 5 to 6 million trades. This is planned capacity, not completed production volume. Resume wording must make that distinction explicit.

## Software Engineer II direction

### 1. Ownership across the settlement platform

Show senior-level ownership across a distributed settlement platform spanning at least five microservices. Focus on cross-service design, integration, production readiness, compatibility with existing consumers, and target scale.

Prefer "distributed settlement platform spanning 5+ microservices" over "federated platform."

The bullet should communicate that Atharva led functional development for the ICB and Nutmeg flow across shared services, while protecting existing business flows. Any reference to 5 to 6 million trades must say "designed for," "targeting," or otherwise make clear that this was projected capacity.

### 2. Automation and defensible LLM work

Atharva deeply owns the end-to-end regression automation framework. This is the best foundation for an AI-engineering-adjacent bullet, but the final wording must reflect code that he actually implemented.

Possible areas to investigate:

- Test generation
- Agent or workflow orchestration
- Failure diagnosis
- Structured model outputs
- Tool use
- Deterministic validation
- Context management
- Evaluation of model-generated results

Do not list a capability until Atharva can explain its architecture, implementation, validation, and limitations in an interview. Keep the automation story in Software Engineer II if it includes meaningful new ownership or LLM integration. Do not repeat the older automation bullet under Software Engineer I.

Historical automation figures need reconciliation before use: about 300 regression scenarios, 30+ developers, 5 teams, and a claimed 90% reduction in manual regression effort.

### 3. DS aggregation engine

DS is the main orchestrator and state manager for a trade throughout its lifecycle. Its aggregation engine, internally called netting, groups trades differently for different business flows using configurable combinations of business dimensions. It then produces consolidated settlement instructions for downstream processing.

Describe the engineering directly instead of using vague phrases such as "stateful trade orchestration" or "configurable workflows."

Promising direction:

> Designed a Java/Spring Boot aggregation engine that grouped high-volume trade streams across configurable dimensions and business flows, producing consolidated downstream settlement instructions.

Strengthen this only after finding a defensible input-to-output reduction, throughput, latency, or operational metric. Do not say the system processed millions of production trades unless production evidence supports it.

### 4. Open senior-level bullet

The fourth bullet is intentionally undecided. It should come from another substantial ownership, architecture, reliability, or performance problem. Do not force a weak OSM bullet to complete the section.

Candidates to investigate:

- Coordination between OSM and the real-time service during end-of-day processing
- Event ordering and concurrent state transitions
- A concrete production-readiness or reliability problem from the ICB rollout
- Cross-service compatibility or migration work not already covered by the first bullet

Only claim that Atharva resolved a race condition if he can describe the exact race, failure mode, and fix.

## Software Engineer I direction

### 1. Matching Service

Keep this story in Software Engineer I. Matching was extracted from the DS/AME monolith and handles inbound market flows using reactive, function-style programming.

Current wording:

> Led the design and migration of a high-throughput microservice from a legacy trade settlement monolith, processing over 700k messages/day, with an event-driven, non-blocking architecture leveraging Kafka and Spring WebFlux for scalability.

Review this for line length and confirm that "led" and 700k messages per day remain defensible. Do not repeat the extraction story under Software Engineer II.

### 2. Kubernetes migration

Current wording:

> Modernized legacy applications by migrating them to an in-house Kubernetes platform, saving $450k annually in infrastructure costs and reducing deployment time by around 50%.

Retain the cost and deployment-time results if they can be supported. Consider naming Java/Spring Boot or the number of applications only if doing so adds useful technical detail and the count is verified.

### 3. Union materialized datastore

Describe Union as a materialized datastore or read model, not as a generic "Client Information Service." It aggregates data from multiple source systems, continuously rehydrates the materialized data, keeps it current with upstream sources, and uses Elasticsearch for fast, complex search.

Preferred direction:

> Architected a materialized datastore using Elasticsearch, aggregating and rehydrating data from multiple source systems to deliver <150 ms search across [X]+ records, enabling the decommissioning of 4 legacy systems.

Preserve the decommissioning result. Confirm the record count before replacing [X]. The old resume said 100K+ records and reduced query time from 2 seconds to under 150 ms; verify whether both figures still describe the final system accurately.

### 4. IGS bulk instruction processing

IGS handles outbound market instructions, including SWIFT messages. It may release millions of instructions in bulk near strict market deadlines. This can become a strong throughput, batching, concurrency, and deadline-reliability story if the implementation and numbers support it.

Before writing the bullet, capture:

- The actual bottleneck or failure risk
- Atharva's design or code changes
- Batching, concurrency, backpressure, retry, or ordering mechanisms used
- Verified volume, duration, latency, or deadline result

If the evidence is weak, replace this with another project Atharva knows deeply.

## Additional project context

OSM and the RT/ARS real-time service coordinate end-of-day processing. The real-time service populates the state and tables that OSM uses, while OSM schedules or orchestrates end-of-day work. This may support a technical story about distributed scheduling, event ordering, concurrent state changes, and coordination between real-time ingestion and batch processing. Claims must be tied to a specific problem Atharva solved.

IGS manages outbound market instructions and SWIFT flows. Matching manages inbound market flows. Union provides a materialized Elasticsearch read model. DS owns trade state and configurable aggregation. The automation framework runs end-to-end regression across services and teams.

## Technology labels

The old role-level labels do not match much of the work described. Reassess them using the final bullets. Likely relevant technologies include:

- Java
- Spring Boot
- Kafka
- Spring WebFlux
- Kubernetes and GKP
- Elasticsearch
- Python, where the automation or LLM implementation supports it
- React, AWS, Terraform, GraphQL, and Splunk only where they reflect material work in the final bullets

Do not keep technologies merely because they appeared in an older version.

## Resume philosophy

Each of the eight bullets needs a distinct job and a credible interview story. Across the section, aim to show:

- Technical ownership and production accountability
- Distributed, stateful processing
- Concurrency and reliability
- Reactive and event-driven architecture
- High-throughput bulk processing
- Search and data architecture
- Kubernetes and infrastructure modernization
- Legitimate AI or LLM engineering work

Seniority should come from scope, architectural decisions, cross-service ownership, production readiness, and technical leadership. It should not depend on inflated language or invented novelty.

## Facts to verify before finalizing

- Final production or tested scale for the ICB and Nutmeg flow
- Whether 5 to 6 million trades refers to daily volume, batch volume, or another interval
- DS input-to-output aggregation ratio or another meaningful performance measure
- Exact capabilities already implemented in the LLM or agentic automation work
- Final regression scenario count, developer count, team count, and manual-effort reduction
- Union record count and whether the 2-second to <150 ms comparison is still accurate
- Matching Service's 700k messages per day and Atharva's exact leadership scope
- Kubernetes savings and deployment-time reduction methodology
- IGS instruction volume, deadline, bottleneck, implementation, and result
- A specific OSM/RT reliability or concurrency problem, if used

## Working process

For each candidate bullet:

1. Capture the problem, Atharva's exact contribution, the implementation, and the result.
2. Separate verified production results from targets, tests, and estimates.
3. Draft one concise bullet with a strong verb and concrete technical language.
4. Check the claim against what Atharva could explain under detailed interview questioning.
5. Compare it with the other seven bullets to remove repeated stories and signals.
6. Keep placeholders such as [X] until the underlying number is verified.

Do not finalize all eight bullets in one pass. Resolve the open facts first, then tighten wording and line length.

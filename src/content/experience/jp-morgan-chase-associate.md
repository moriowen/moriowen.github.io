---
title: JP Morgan Chase
subtitle: Mumbai, India
meta: Jan 2026 - Jul 2026
order: 1
summary: >-
  Worked on a new business flow across a seven-service settlement platform. Helped set up an
  agent-assisted development workflow, built a Groovy E2E framework covering 300+ fixed-income
  scenarios, and implemented a netting aggregator to reduce settlement instructions.
contents:
  - heading: "The settlement workflow"
    description: "How a trade moves through AME to the market and back."
  - heading: "A new business flow on a shared platform"
    description: "Adapted a new flow across seven existing services."
  - heading: "An agent-assisted Jira-to-PR workflow"
    description: "Set up shared context and local-testing integration for Claude Code."
  - heading: "E2E regression across 300+ scenarios"
    description: "Built the Groovy framework for message replay and database checks."
  - heading: "Netting trades into fewer instructions"
    description: "Aggregated compatible trades before scheduled release."
roles:
  - title: Software Engineer II (Associate)
    when: Jan 2026 - Jul 2026
    where: Mumbai
    bullets:
      - Contributed to cross-service design and production readiness for a new business flow on an established seven-service settlement platform, adapting new behavior while preserving existing business flows.
      - Helped set up a Claude Code development workflow with shared service documentation, local-testing integration and colleague onboarding; Jira MCP supplied requirements and Bitbucket MCP opened PRs, with notifications in Symphony.
      - Built a Groovy E2E testing framework covering 300+ fixed-income scenarios through message replay, MQ and Kafka connections, and database assertions; its use became mandatory across a team of roughly 50 people.
      - Implemented a settlement netting aggregator with configurable grouping dimensions, periodic aggregation and scheduled release, reducing settlement instruction volume by approximately 70%.
---

## The settlement workflow

Asset Movement Engine was the seven-service settlement platform I worked on. Its main flow
turned trades into market instructions and matched incoming confirmations back to trade state.

<figure class="architecture-diagram">
<p class="architecture-label">Settlement platform</p>
<picture>
<source media="(max-width: 34rem)" srcset="/diagrams/ame-settlement-mobile.svg" />
<img src="/diagrams/ame-settlement.svg" alt="Settlement platform: Trade input; Settlement state; Outbound gateway; Downstream services; Matching service; Market / SWIFT MQ. Arrows show component connections." width="760" height="324" loading="lazy" />
</picture>
<figcaption>Simplified straight-through processing flow. Business-line rules add branches to this path.</figcaption>
</figure>

I worked on Asset Movement Engine, a settlement platform that evolved from a monolith into seven
services. Five handled the main processing flow and two handled end-of-day work. A trade entered
through the service responsible for trade state, became a settlement instruction, and went through
an outbound gateway that converted it into a SWIFT message for the market. Incoming market
confirmations and status updates took the return path through matching and back into trade state.



## A new business flow on a shared platform

I helped adapt a new business flow across existing services, working on business requirements,
cross-service behavior and production readiness.

<figure class="architecture-diagram">
<p class="architecture-label">New business flow on shared infrastructure</p>
<picture>
<source media="(max-width: 34rem)" srcset="/diagrams/ame-business-flow-mobile.svg" />
<img src="/diagrams/ame-business-flow.svg" alt="New business flow on shared infrastructure: New business flow; Shared AME platform; Existing business lines; Regression framework; Readiness work. Arrows show component connections." width="760" height="324" loading="lazy" />
</picture>
<figcaption>The design targeted projected growth. Regression coverage connected business requirements to platform readiness.</figcaption>
</figure>

My work was product-facing engineering: understanding the business flow, helping adapt it across
shared services, and supporting production readiness. Much of the platform code already existed
and had been running for years. Changes for one line of business had to coexist with the behavior
other business lines already depended on.

The projected load was roughly five to six million trades. I left before that volume arrived, so
it remained a design target when I left.
The important challenge was coordinating the new behavior across an established platform while
preserving existing business rules.

## An agent-assisted Jira-to-PR workflow

I helped set up a Claude Code development workflow, contributing the shared documentation
structure, local-testing integration and guidance for colleagues.

<figure class="architecture-diagram">
<p class="architecture-label">Agent-assisted development architecture</p>
<picture>
<source media="(max-width: 34rem)" srcset="/diagrams/ame-adlc-mobile.svg" />
<img src="/diagrams/ame-adlc.svg" alt="Agent-assisted development architecture: Jira MCP; Shared ADLC repo; Local repositories; Groovy framework; Claude Code; Bitbucket MCP; Local service setup; Symphony. Arrows show component connections." width="760" height="484" loading="lazy" />
</picture>
<figcaption>The shared context and test framework supported changes across the service repositories.</figcaption>
</figure>

I was one of the engineers helping set up this effort alongside senior engineers and architects.
My contributions were the shared documentation structure, integration of local testing, and
helping colleagues use Claude Code with the services. Other contributors handled service startup
and containerization. The local setup included both Dockerized and non-containerized services;
the older settlement-state service was particularly difficult to run locally.

Each team contributed service documentation and differences between business lines to a common
agent-development repository. When adding behavior to one business line, the agent could consult
related behavior in another instead of relying on a single service's code. The challenge was
maintaining useful business context while the services and workflows kept changing.

This was an ongoing, collaborative project. We iterated on the documentation and setup as the
team used it. My strongest implementation contribution was the testing framework below.

## E2E regression across 300+ scenarios

I built a Groovy framework to replay messages through settlement workflows and check database
outcomes across more than 300 fixed-income scenarios.

<figure class="architecture-diagram">
<p class="architecture-label">E2E regression test architecture</p>
<picture>
<source media="(max-width: 34rem)" srcset="/diagrams/ame-regression-mobile.svg" />
<img src="/diagrams/ame-regression.svg" alt="E2E regression test architecture: 300+ scenarios; Groovy framework; Failure reporting; MQ / Kafka; AME services; Service databases. Arrows show component connections." width="760" height="324" loading="lazy" />
</picture>
<figcaption>The framework drove real services in dev and later locally. Independent work could run in parallel.</figcaption>
</figure>

I built a Groovy framework that drove settlement workflows by playing sets of messages,
connecting to message queues and Kafka brokers, and fetching or saving data in databases. It
initially ran against services in the development environment and was later integrated with local
services. Groovy was required by the framework we chose; an internal reporting tool also let us
email stakeholders when important tests failed.

The difficult part was translating financial behavior into assertions. A small change in an input
field could alter charges, settlement amounts and netting farther along the flow. I had to trace
those effects across service contracts and database tables, then cover more than 300 scenarios
for a fixed-income line of business. My end-to-end knowledge of the platform mattered as much as
the test code.

Service updates were asynchronous, so the framework polled for results. We also used parallel
execution to address runtime: a long regression run was expensive to repeat before a production
release. I used early Claude models extensively during development; later local setup work used
Claude Code with API access.

By my departure, use of the system was mandatory and roughly 50 people interacted with it in
some way. The move toward local-first testing let us exercise more scenarios earlier; I observed fewer errors, but do not
have a measured error-reduction percentage.

## Netting trades into fewer instructions

I implemented the aggregator that grouped eligible trades into net settlement instructions,
reducing the volume sent downstream for conversion into SWIFT messages.

<figure class="architecture-diagram">
<p class="architecture-label">Netting aggregation architecture</p>
<picture>
<source media="(max-width: 34rem)" srcset="/diagrams/ame-netting-mobile.svg" />
<img src="/diagrams/ame-netting.svg" alt="Netting aggregation architecture: Trade table; Netting aggregator; Grouping rules; Aggregation scheduler; Scheduled release; Outbound processing. Arrows show component connections." width="760" height="324" loading="lazy" />
</picture>
<figcaption>Grouping and frequent aggregation are separate from the scheduled release.</figcaption>
</figure>

I implemented the aggregator that consolidated eligible trades into net settlement instructions.
For example, two eligible obligations of 100 and 50 in opposite directions can become one net
obligation of 50. This reduces the instructions sent downstream for conversion into SWIFT
messages, while retaining the underlying trade records.

Different netting types and business lines had different grouping rules. The main challenge was
getting the arithmetic and edge cases right without breaking the existing aggregation engine.
One example was a zero-net group, where buys and sells canceled and could not produce a
zero-value market instruction.

The project estimate was approximately 70% fewer settlement instructions, reducing the volume
sent to downstream processing.

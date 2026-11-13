---
title: JP Morgan Chase
subtitle: Mumbai, India
meta: Jan 2026 - Jul 2026
order: 1
summary: >-
  Worked on a new business flow across a seven-service settlement platform. Helped set up an
  agent-assisted development workflow, built a Groovy E2E framework covering 300+ fixed-income
  scenarios, and implemented a netting aggregator to reduce settlement instructions.
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

I worked on Asset Movement Engine, a settlement platform that evolved from a monolith into seven
services. Five handled the main processing flow and two handled end-of-day work. A trade entered
through the service responsible for trade state, became a settlement instruction, and went through
an outbound gateway that converted it into a SWIFT message for the market. Incoming market
confirmations and status updates took the return path through matching and back into trade state.

<figure class="system-flow">
<p class="system-flow-label">Trade to market, then back to trade state</p>
<ol aria-label="Trade to market, then back to trade state">
<li><strong>Trade input</strong><span>A reduced trade message enters the platform.</span></li>
<li><strong>Settlement state</strong><span>Process the trade and produce a settlement instruction.</span></li>
<li><strong>Outbound gateway</strong><span>Convert the instruction to SWIFT and send it to the market.</span></li>
<li><strong>Market update</strong><span>A confirmation or status update arrives through a message queue.</span></li>
<li><strong>Matching and state</strong><span>Identify the trade, update its state and notify downstream services.</span></li>
</ol>
<figcaption>Simplified straight-through processing flow. Business-line rules add branches to this path.</figcaption>
</figure>

## A new business flow on a shared platform

My work was product-facing engineering: understanding the business flow, helping adapt it across
shared services, and supporting production readiness. Much of the platform code already existed
and had been running for years. Changes for one line of business had to coexist with the behavior
other business lines already depended on.

<figure class="system-flow">
<p class="system-flow-label">Adapting an existing platform</p>
<ol aria-label="Adapting an existing platform">
<li><strong>Business requirements</strong><span>Understand the new flow and its financial rules.</span></li>
<li><strong>Shared-service changes</strong><span>Fit the flow into existing service contracts and behavior.</span></li>
<li><strong>Regression coverage</strong><span>Exercise the new scenarios alongside existing business flows.</span></li>
<li><strong>Production readiness</strong><span>Support integration and readiness for the new business.</span></li>
</ol>
<figcaption>The design targeted projected growth. Regression coverage connected business requirements to platform readiness.</figcaption>
</figure>

The projected load was roughly five to six million trades. I left before that volume arrived, so
it remained a design target when I left.
The important challenge was coordinating the new behavior across an established platform while
preserving existing business rules.

## An agent-assisted Jira-to-PR workflow

I was one of the engineers helping set up this effort alongside senior engineers and architects.
My contributions were the shared documentation structure, integration of local testing, and
helping colleagues use Claude Code with the services. Other contributors handled service startup
and containerization. The local setup included both Dockerized and non-containerized services;
the older settlement-state service was particularly difficult to run locally.

<figure class="system-flow">
<p class="system-flow-label">Requirements to a reviewable change</p>
<ol aria-label="Requirements to a reviewable change">
<li><strong>Jira MCP</strong><span>Fetch the ticket requirements.</span></li>
<li><strong>Claude Code and context</strong><span>Use local repositories and shared service documentation to make changes.</span></li>
<li><strong>Local testing</strong><span>Exercise business scenarios with the Groovy framework.</span></li>
<li><strong>Bitbucket MCP</strong><span>Open a PR for the pushed code changes.</span></li>
<li><strong>Symphony</strong><span>Existing repository automation posts the PR to team chat.</span></li>
</ol>
<figcaption>The shared context and test framework supported changes across the service repositories.</figcaption>
</figure>

Each team contributed service documentation and differences between business lines to a common
agent-development repository. When adding behavior to one business line, the agent could consult
related behavior in another instead of relying on a single service's code. The challenge was
maintaining useful business context while the services and workflows kept changing.

This was an ongoing, collaborative project. We iterated on the documentation and setup as the
team used it. My strongest implementation contribution was the testing framework below.

## E2E regression across 300+ scenarios

I built a Groovy framework that drove settlement workflows by playing sets of messages,
connecting to message queues and Kafka brokers, and fetching or saving data in databases. It
initially ran against services in the development environment and was later integrated with local
services. Groovy was required by the framework we chose; an internal reporting tool also let us
email stakeholders when important tests failed.

<figure class="system-flow">
<p class="system-flow-label">One regression scenario</p>
<ol aria-label="One regression scenario">
<li><strong>Scenario and messages</strong><span>Supply a trade and the messages required by the business case.</span></li>
<li><strong>Service processing</strong><span>Exercise the settlement workflow through MQ, Kafka and service data.</span></li>
<li><strong>Poll database state</strong><span>Wait for asynchronous processing and check tables in sequence.</span></li>
<li><strong>Assertions and reporting</strong><span>Compare the resulting data with expected outcomes and report failures.</span></li>
</ol>
<figcaption>The framework drove real services in dev and later locally. Independent work could run in parallel.</figcaption>
</figure>

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

I implemented the aggregator that consolidated eligible trades into net settlement instructions.
For example, two eligible obligations of 100 and 50 in opposite directions can become one net
obligation of 50. This reduces the instructions sent downstream for conversion into SWIFT
messages, while retaining the underlying trade records.

<figure class="system-flow">
<p class="system-flow-label">Aggregation and release</p>
<ol aria-label="Aggregation and release">
<li><strong>Trade table</strong><span>Hold trades eligible for aggregation.</span></li>
<li><strong>Netting ID</strong><span>Derive the grouping key from multiple business fields.</span></li>
<li><strong>Periodic aggregation</strong><span>Aggregate compatible trades roughly every five seconds.</span></li>
<li><strong>Scheduled release</strong><span>Release instructions about one hour before end of day.</span></li>
<li><strong>Outbound processing</strong><span>Send fewer consolidated instructions toward the market.</span></li>
</ol>
<figcaption>Grouping and frequent aggregation are separate from the scheduled release.</figcaption>
</figure>

Different netting types and business lines had different grouping rules. The main challenge was
getting the arithmetic and edge cases right without breaking the existing aggregation engine.
One example was a zero-net group, where buys and sells canceled and could not produce a
zero-value market instruction.

The project estimate was approximately 70% fewer settlement instructions, reducing the volume
sent to downstream processing.

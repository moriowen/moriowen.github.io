---
title: JP Morgan Chase
subtitle: Mumbai, India
meta: Jun 2023 - Jan 2026
order: 2
summary: >-
  Generalized a Kafka and WebFlux matching service for reuse across business lines, worked on
  end-of-day bulk dispatch, and implemented most of a client-data service with sub-150ms search.
  Also assisted senior engineers with the team's Kubernetes migration.
contents:
  - heading: "Generalizing the matching service"
    description: "Extended business-specific processing for reuse across business lines."
  - heading: "End-of-day bulk message dispatch"
    description: "Worked on concurrent publishing, memory issues and safe work pickup."
  - heading: "Consolidated client-data search"
    description: "Built search over a Kafka-maintained Elasticsearch read layer."
  - heading: "Supporting the Kubernetes migration"
    description: "Assisted senior engineers with the move to the internal platform."
roles:
  - title: Software Engineer I (Analyst)
    when: Jun 2023 - Jan 2026
    where: Mumbai
    bullets:
      - Contributed to the design and implementation of a reusable Kafka and Spring WebFlux matching service, generalizing an existing business-specific implementation for other lines of business.
      - Worked on multithreaded end-of-day dispatch of millions of messages from database records to downstream queues, debugging memory issues and addressing concurrent work pickup across pods.
      - Implemented most of a client-data service, with primary ownership of search and query construction over an Elasticsearch read layer maintained through asynchronous Kafka updates, supporting sub-150ms searches.
      - Assisted senior engineers with migration to the firm's internal Kubernetes platform as part of a team initiative reporting approximately $450k in annual infrastructure savings.
---

## Generalizing the matching service

I helped generalize the Kafka and WebFlux matching service from a single-business-line
implementation into reusable processing for other business lines.

<figure class="architecture-diagram">
<p class="architecture-label">Reusable matching-service architecture</p>
<picture>
<source media="(max-width: 34rem)" srcset="/diagrams/ame-matching-mobile.svg" />
<img src="/diagrams/ame-matching.svg" alt="Reusable matching-service architecture: Market messages; Kafka / WebFlux service; Settlement state; External data services; Composable functions; Business-line behavior. Arrows show component connections." width="760" height="324" loading="lazy" />
</picture>
<figcaption>Kafka and Spring WebFlux supported the matching service; common processing was designed for reuse.</figcaption>
</figure>

The matching service received SWIFT confirmations and status updates from the market and
identified the corresponding trade. It was part of the work to split the settlement monolith into
services. I joined roughly six months after the project started, when the implementation was
specific to one line of business. My assignment was to help make it reusable by other business
lines.

I contributed to the design and wrote substantial implementation code. We organized processing
as composable functions: enrich a message, transform its data, and pass the result into the next
step. The purpose was to share common processing rather than copy an entire workflow for each
business line.

The challenge was separating reusable processing from the business-specific behavior in an
existing implementation. The design goal was a shared implementation that could support additional business lines.

## End-of-day bulk message dispatch

I worked on multithreaded dispatch of millions of end-of-day messages, debugging memory
problems and coordinating database work pickup across pods.

<figure class="architecture-diagram">
<p class="architecture-label">Concurrent end-of-day dispatch</p>
<picture>
<source media="(max-width: 34rem)" srcset="/diagrams/ame-eod-mobile.svg" />
<img src="/diagrams/ame-eod.svg" alt="Concurrent end-of-day dispatch: EOD message; Service pod A; Message broker; Database work; Service pod B; Downstream services. Arrows show component connections." width="760" height="324" loading="lazy" />
</picture>
<figcaption>Coordination between workers prevented pods from claiming the same work concurrently.</figcaption>
</figure>

An end-of-day message triggered a large database-to-queue workload. Millions of messages needed
to reach downstream services in a short window. We used multithreaded processing to retrieve
data and publish messages quickly, with multiple pods of the same service working concurrently.

I worked on this dispatch flow and personally debugged memory problems. Another challenge was
race conditions when pods tried to pick up the same database work. We implemented coordination
that let pods pick up and process different work concurrently.

The engineering problem was balancing throughput, memory use and safe work pickup under a tight
release window. Sending work to the queue was only this service's part of downstream processing.

## Consolidated client-data search

I implemented most of a client-data service, with primary ownership of search and query
construction over an Elasticsearch layer that supported sub-150ms retrieval.

<figure class="architecture-diagram">
<p class="architecture-label">Client-data search architecture</p>
<picture>
<source media="(max-width: 34rem)" srcset="/diagrams/ame-search-mobile.svg" />
<img src="/diagrams/ame-search.svg" alt="Client-data search architecture: Reference services; Kafka events; Consolidated database; Search clients; Search component; Elasticsearch. Arrows show component connections." width="760" height="324" loading="lazy" />
</picture>
<figcaption>The search view could lag source updates. Read requests were synchronous; update processing was separate.</figcaption>
</figure>

This service brought together client data from multiple reference-data providers. The source
structure was complex, and assembling a complete client view otherwise required several table
joins. We used Elasticsearch as a search layer over the database, with precomputed data organized
for retrieval.

I implemented most of the service, with primary ownership of the search component and query
construction. The search path delivered sub-150ms retrieval. The result depended on both the
stored representation and the queries used to retrieve it, rather than Elasticsearch alone.

The main integration challenge was freshness across different providers. Each sent Kafka events
when its data changed, and our service had to accommodate different contracts while keeping the
consolidated view current. Immediate visibility of every update was not required, which let us
separate asynchronous maintenance from synchronous reads.

This is one of the projects I am proudest of: I took substantial implementation ownership while
working alongside more senior engineers, and learned how data modeling and query construction
shape a service's read performance.

## Supporting the Kubernetes migration

I assisted senior engineers with migrating services from on-premises infrastructure to the
firm's internal Kubernetes platform.

<figure class="architecture-diagram">
<p class="architecture-label">Team Kubernetes migration</p>
<picture>
<source media="(max-width: 34rem)" srcset="/diagrams/ame-kubernetes-mobile.svg" />
<img src="/diagrams/ame-kubernetes.svg" alt="Team Kubernetes migration: Existing services; Container images; Internal Kubernetes; Senior engineers; My contribution. Arrows show component connections." width="760" height="324" loading="lazy" />
</picture>
<figcaption>I assisted the migration. Platform design, containerization and the overall result were team work.</figcaption>
</figure>

I assisted senior engineers with the team's move from on-premises infrastructure to an internal
Kubernetes platform. The migration included containerizing services so they could run in pods.
I was early in my development career, and most of the migration work was led and implemented by
senior engineers.

The initiative reported approximately $450k in annual infrastructure savings. That was the team's
result, not savings I delivered individually. I treat this as supporting infrastructure
experience, alongside the projects where I had deeper implementation ownership.

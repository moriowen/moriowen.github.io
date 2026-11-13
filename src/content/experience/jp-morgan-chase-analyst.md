---
title: JP Morgan Chase
subtitle: Mumbai, India
meta: Jun 2023 - Jan 2026
order: 2
summary: >-
  Generalized a Kafka and WebFlux matching service for reuse across business lines, worked on
  end-of-day bulk dispatch, and implemented most of a client-data service with sub-150ms search.
  Also assisted senior engineers with the team's Kubernetes migration.
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

The matching service received SWIFT confirmations and status updates from the market and
identified the corresponding trade. It was part of the work to split the settlement monolith into
services. I joined roughly six months after the project started, when the implementation was
specific to one line of business. My assignment was to help make it reusable by other business
lines.

<figure class="system-flow">
<p class="system-flow-label">Matching as a composable processing pipeline</p>
<ol aria-label="Matching as a composable processing pipeline">
<li><strong>Market message</strong><span>Receive a confirmation or status update.</span></li>
<li><strong>Enrichment</strong><span>Fetch additional data from other services.</span></li>
<li><strong>Transformation</strong><span>Compose processing steps into the downstream message contract.</span></li>
<li><strong>Trade matching</strong><span>Identify the trade and send its update to settlement state.</span></li>
</ol>
<figcaption>Kafka and Spring WebFlux supported the matching service; common processing was designed for reuse.</figcaption>
</figure>

I contributed to the design and wrote substantial implementation code. We organized processing
as composable functions: enrich a message, transform its data, and pass the result into the next
step. The purpose was to share common processing rather than copy an entire workflow for each
business line.

The challenge was separating reusable processing from the business-specific behavior in an
existing implementation. The design goal was a shared implementation that could support additional business lines.

## End-of-day bulk message dispatch

An end-of-day message triggered a large database-to-queue workload. Millions of messages needed
to reach downstream services in a short window. We used multithreaded processing to retrieve
data and publish messages quickly, with multiple pods of the same service working concurrently.

<figure class="system-flow">
<p class="system-flow-label">Concurrent end-of-day dispatch</p>
<ol aria-label="Concurrent end-of-day dispatch">
<li><strong>EOD trigger</strong><span>Start the end-of-day workload.</span></li>
<li><strong>Database work</strong><span>Identify records awaiting dispatch.</span></li>
<li><strong>Concurrent workers</strong><span>Coordinate pickup across pods and process work in parallel.</span></li>
<li><strong>Message broker</strong><span>Publish messages for downstream end-of-day processing.</span></li>
</ol>
<figcaption>Coordination between workers prevented pods from claiming the same work concurrently.</figcaption>
</figure>

I worked on this dispatch flow and personally debugged memory problems. Another challenge was
race conditions when pods tried to pick up the same database work. We implemented coordination
that let pods pick up and process different work concurrently.

The engineering problem was balancing throughput, memory use and safe work pickup under a tight
release window. Sending work to the queue was only this service's part of downstream processing.

## Consolidated client-data search

This service brought together client data from multiple reference-data providers. The source
structure was complex, and assembling a complete client view otherwise required several table
joins. We used Elasticsearch as a search layer over the database, with precomputed data organized
for retrieval.

<figure class="system-flow">
<p class="system-flow-label">Asynchronous updates, synchronous search</p>
<ol aria-label="Asynchronous updates, synchronous search">
<li><strong>Reference services</strong><span>Provide client data through different source contracts.</span></li>
<li><strong>Kafka change events</strong><span>Signal source updates asynchronously.</span></li>
<li><strong>Consolidated read layer</strong><span>Maintain client data in the database and Elasticsearch search view.</span></li>
<li><strong>Synchronous search</strong><span>Build queries and return the consolidated client view.</span></li>
</ol>
<figcaption>The search view could lag source updates. Read requests were synchronous; update processing was separate.</figcaption>
</figure>

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

I assisted senior engineers with the team's move from on-premises infrastructure to an internal
Kubernetes platform. The migration included containerizing services so they could run in pods.
I was early in my development career, and most of the migration work was led and implemented by
senior engineers.

<figure class="system-flow">
<p class="system-flow-label">Team migration to Kubernetes</p>
<ol aria-label="Team migration to Kubernetes">
<li><strong>Existing services</strong><span>Applications on the previous infrastructure.</span></li>
<li><strong>Containerization</strong><span>Package services to run in containers.</span></li>
<li><strong>Internal Kubernetes</strong><span>Run the applications as workloads in pods.</span></li>
</ol>
<figcaption>I assisted the migration. Platform design, containerization and the overall result were team work.</figcaption>
</figure>

The initiative reported approximately $450k in annual infrastructure savings. That was the team's
result, not savings I delivered individually. I treat this as supporting infrastructure
experience, alongside the projects where I had deeper implementation ownership.

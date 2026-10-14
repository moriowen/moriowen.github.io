---
title: JP Morgan Chase
subtitle: Mumbai, India
meta: Jun 2023 - Jan 2026
order: 2
summary: >-
  Two and a half years on trade settlement infrastructure. Extracted a Kafka and WebFlux service
  from the settlement monolith, orchestrated end-of-day processing under a 30-minute cutoff,
  replaced four legacy systems with one Elasticsearch-backed datastore, and moved 15 applications
  onto Kubernetes.
roles:
  - title: Software Engineer I (Analyst)
    when: Jun 2023 - Jan 2026
    where: Mumbai
    bullets:
      - Led extraction of a high-throughput microservice from a legacy trade settlement monolith, processing 1M+ messages per day, with an event-driven, non-blocking stack with Kafka and Spring WebFlux.
      - Designed distributed end-of-day orchestration coordinating 3 services to close and settle the day's book within a 30-minute cutoff, handling race conditions, ordering dependencies, and concurrent state transitions with idempotent replay on failure.
      - Architected a materialized datastore using Elasticsearch, aggregating and rehydrating data from multiple source systems to provide sub-150ms complex search over 750k records, enabling the decommission of 4 legacy systems.
      - Migrated 15 legacy applications to an in-house Kubernetes platform, saving $450k annually in infrastructure costs and reducing deployment time by 50%.
---

## Breaking up the monolith

The service handles inbound messages from the market. I pulled it out of the monolith that owns
trade state and rewrote it in a reactive, functional style on Spring WebFlux.

TODO: what made this service the right one to extract first. The seam you cut along, how you
migrated traffic without a big-bang cutover, and what you would do differently. Kafka and Spring
WebFlux were the stack, so the backpressure story belongs here too.

## End-of-day orchestration

TODO: the strongest distributed systems story you have. A 30-minute cutoff across 3 services with
ordering dependencies and real money on the line. The failure modes you designed around, why
idempotent replay was the right answer, and what a bad day looked like.

## The materialized datastore

750k records, sub-150ms complex search, four legacy systems retired.

It is a read model in Elasticsearch. It pulls from several source systems and rehydrates
continuously to stay current with them.

TODO: why the source systems could not answer these queries themselves, how you kept the
materialized view consistent with its sources as it rehydrated, and what made the nesting the hard
part.

## Kubernetes migration

The applications moved off legacy virtual machines onto the firm's internal Kubernetes platform,
and I worked on the first rollout to it.

TODO: what made 15 migrations tractable, and where the $450k came from.

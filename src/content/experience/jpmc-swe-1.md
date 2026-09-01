---
title: Software Engineer I
subtitle: JP Morgan Chase
meta: Feb 2023 - Dec 2025
order: 2
summary: >-
  Three years pulling a trade settlement monolith apart: extracting services, orchestrating
  end-of-day under a hard cutoff, and making 750k records searchable in under 150ms.
bullets:
  - Led extraction of a high-throughput microservice from a legacy trade settlement monolith, processing 1M+ messages per day on an event-driven, non-blocking stack with Kafka and Spring WebFlux.
  - Designed distributed end-of-day orchestration coordinating 3 services to close and settle the day's book within a 30-minute cutoff, handling race conditions, ordering dependencies, and concurrent state transitions with idempotent replay on failure.
  - Architected a materialized datastore in Elasticsearch, aggregating and rehydrating data from multiple source systems for sub-150ms complex search over 750k records, enabling the decommission of 4 legacy systems.
  - Migrated 15 legacy applications to an in-house Kubernetes platform, saving $450k annually in infrastructure costs and cutting deployment time by 50%.
---

## Breaking up the monolith

TODO: what made this service the right one to extract first. The seam you cut along, how you
migrated traffic without a big-bang cutover, and what you would do differently.

## End-of-day orchestration

TODO: the most technically interesting problem. A 30-minute cutoff across 3 services with ordering
dependencies is a distributed systems problem with real money on the line. Explain the failure
modes you had to design around, why idempotent replay was the right answer, and what a bad day
looked like.

## The Elasticsearch materialized view

TODO: why the source systems could not answer these queries themselves. How you kept the
materialized view consistent with its sources, what rehydration means here, and how decommissioning
4 systems was justified.

## Kubernetes migration

TODO: 15 applications is a lot of migrations. What made it tractable, and where the $450k came from.

---
title: JP Morgan Chase
subtitle: Mumbai and Bengaluru, India
meta: Jan 2022 - Jul 2026
order: 1
summary: >-
  Three and a half years across two internships and two engineering roles, most of it on trade
  settlement infrastructure: extracting services from a monolith, orchestrating end-of-day
  processing under a hard cutoff, and replacing four legacy systems with one search-backed
  datastore.
roles:
  - title: Software Engineer II
    when: Jan 2026 - Jul 2026
    where: Mumbai
    bullets:
      - Owned cross-service design and production readiness for a new business line across 7 microservices on a multi-tenant settlement platform, scaling throughput to 5M+ trades per day.
      - Designed a Spring Boot aggregation engine that folds high-volume trade streams into consolidated settlement instructions across configurable dimensions, cutting instruction volume by 70%.
      - Built an LLM-agent regression framework that generates and diagnoses multi-service test workflows, automating 300+ scenarios and cutting manual test effort 90%. Adopted by 30+ engineers across 5 teams.
  - title: Software Engineer I
    when: Jun 2023 - Jan 2026
    where: Mumbai
    bullets:
      - Led the design and extraction of a high-throughput microservice from a legacy trade settlement monolith, processing over 700k messages per day and improving modularity, testability, and fault isolation.
      - Architected and delivered a scalable Client Information Service managing 100K+ deeply nested records, decommissioning 4 legacy systems and cutting average query time from 2s to under 150ms with Elasticsearch. Recognized publicly by an Executive Director at the SEP cohort meet for this work.
      - Designed distributed end-of-day orchestration coordinating 3 services to close and settle the day's book within a 30-minute cutoff, handling race conditions, ordering dependencies, and concurrent state transitions with idempotent replay on failure.
      - Modernized legacy applications by migrating them to an in-house Kubernetes platform, saving $450k in infrastructure costs and reducing deployment time by around 50%.
  - title: Software Engineer Intern
    when: Feb 2023 - May 2023
    where: Mumbai
    bullets:
      - Built and maintained an internal UI design system used by 6+ teams, cutting UI development effort across the line of business by 30-40% through reusable components and templates.
      - Designed reusable, config-driven microservices and libraries orchestrating data flows with Kafka and GraphQL, reducing duplicate integration effort across 5+ services.
  - title: Software Engineer Intern
    when: Jan 2022 - Jul 2022
    where: Bengaluru
    bullets:
      - Developed a monitoring framework that identified and decommissioned 50+ unused resources across 20+ AWS accounts using Terraform APIs and AWS resource tagging.
      - Built Splunk dashboards visualizing inventory, enabling data-driven cleanup decisions and projected savings of $10K+ annually.
---

## The domain

TODO: describe trade settlement in a paragraph a non-specialist can follow. What a settlement
instruction is, why volume matters, and what breaks when it goes wrong.

## Launching a new business line

Seven microservices on a multi-tenant platform, scaled to 5M+ trades per day.

TODO: what "production readiness" meant concretely, what you owned versus influenced, and the
hardest design call you had to make.

## The aggregation engine

TODO: why 70% fewer instructions matters downstream. What the configurable dimensions are, and why
the correct grouping was not obvious.

## LLM agents for regression testing

TODO: the most interesting thing here. What the agent actually does, why a generated suite beats a
handwritten one for multi-service workflows, where it fails, and how you got 30+ engineers on 5
teams to trust it.

## Breaking up the monolith

TODO: what made this service the right one to extract first. The seam you cut along, how you
migrated traffic without a big-bang cutover, and what you would do differently.

## End-of-day orchestration

TODO: the strongest distributed systems story you have. A 30-minute cutoff across 3 services with
ordering dependencies and real money on the line. The failure modes you designed around, why
idempotent replay was the right answer, and what a bad day looked like.

## The Client Information Service

100K+ deeply nested records, 2s down to under 150ms, four legacy systems retired.

TODO: why the source systems could not answer these queries themselves, how you kept the
materialized view consistent with its sources, and what made the nesting the hard part.

## Kubernetes migration

TODO: what made 15 migrations tractable, and where the $450k came from.

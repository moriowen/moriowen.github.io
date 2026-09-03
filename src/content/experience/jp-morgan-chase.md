---
title: JP Morgan Chase
subtitle: Mumbai and Bengaluru, India
meta: Jan 2022 - Jul 2026
order: 1
summary: >-
  Three and a half years across two internships and two engineering roles, most of it on trade
  settlement infrastructure: extracting services from a monolith, orchestrating end-of-day
  processing under a hard cutoff, replacing four legacy systems with one search-backed
  datastore, and putting LLM agents to work on testing and the SDLC itself.
roles:
  - title: Software Engineer II
    when: Jan 2026 - Jul 2026
    where: Mumbai
    bullets:
      - Owned cross-service design and production readiness for a new business line across 7 microservices on a multi-tenant settlement platform, scaling throughput to 5M+ trades per day.
      - Built an agentic SDLC pipeline that autonomously translated Jira requirements into code changes across a multi-service architecture, reproduced issues with local infrastructure, validated via automated tests, and raised developer-ready PRs for review, with 75% PRs merged with minimal edits.
      - Built a regression framework using LLM agents that generates and diagnoses multi-service test workflows, automating 300+ scenarios and cutting manual test effort by 90%; adopted by 30+ engineers across 5 teams.
      - Designed an aggregation engine in Spring Boot reducing high-volume trade streams into consolidated settlement instructions across configurable dimensions, cutting down instruction volume by 70%.
  - title: Software Engineer I
    when: Jun 2023 - Jan 2026
    where: Mumbai
    bullets:
      - Led extraction of a high-throughput microservice from a legacy trade settlement monolith, processing 1M+ messages per day, with an event-driven, non-blocking stack with Kafka and Spring WebFlux.
      - Designed distributed end-of-day orchestration coordinating 3 services to close and settle the day's book within a 30-minute cutoff, handling race conditions, ordering dependencies, and concurrent state transitions with idempotent replay on failure.
      - Architected a materialized datastore using Elasticsearch, aggregating and rehydrating data from multiple source systems to provide sub-150ms complex search over 750k records, enabling the decommission of 4 legacy systems.
      - Migrated 15 legacy applications to an in-house Kubernetes platform, saving $450k annually in infrastructure costs and reducing deployment time by 50%.
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
      - Developed a cloud resource discovery framework that helped discover 10k+ resources, consolidating AWS Config, Splunk, Terraform, and tagging APIs into a unified inventory using Qlik Sense dashboards for tracking resource ownership, enabling data-driven cleanup decisions and improving infrastructure visibility for the DevOps team.
---

## The domain

TODO: describe trade settlement in a paragraph a non-specialist can follow. What a settlement
instruction is, why volume matters, and what breaks when it goes wrong.

## Launching a new business line

Seven microservices on a multi-tenant platform, scaled to 5M+ trades per day.

TODO: what "production readiness" meant concretely, what you owned versus influenced, and the
hardest design call you had to make.

## An agentic SDLC pipeline

Jira ticket in, developer-ready PR out, across a multi-service architecture. 75% merged with
minimal edits.

TODO: the pitch is easy and the detail is what matters. How the agent reproduces an issue against
local infrastructure, what stops it from confidently shipping something wrong, what the other 25%
of PRs get wrong, and what a human still has to do.

## LLM agents for regression testing

TODO: the most interesting thing here. What the agent actually does, why a generated suite beats a
handwritten one for multi-service workflows, where it fails, and how you got 30+ engineers on 5
teams to trust it.

## The aggregation engine

TODO: why 70% fewer instructions matters downstream. What the configurable dimensions are, and why
the correct grouping was not obvious.

## Breaking up the monolith

TODO: what made this service the right one to extract first. The seam you cut along, how you
migrated traffic without a big-bang cutover, and what you would do differently. Kafka and Spring
WebFlux were the stack, so the backpressure story belongs here too.

## End-of-day orchestration

TODO: the strongest distributed systems story you have. A 30-minute cutoff across 3 services with
ordering dependencies and real money on the line. The failure modes you designed around, why
idempotent replay was the right answer, and what a bad day looked like.

## The materialized datastore

750k records, sub-150ms complex search, four legacy systems retired.

TODO: why the source systems could not answer these queries themselves, how you kept the
materialized view consistent with its sources as it rehydrated, and what made the nesting the hard
part.

## Kubernetes migration

TODO: what made 15 migrations tractable, and where the $450k came from.

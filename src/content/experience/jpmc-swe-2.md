---
title: Software Engineer II
subtitle: JP Morgan Chase
meta: Jan 2026 - Aug 2026
order: 1
summary: >-
  Owned design and production readiness for a new business line on a multi-tenant trade
  settlement platform, and built the LLM-agent test framework the wider org now runs on.
bullets:
  - Owned cross-service design and production readiness for a new business line across 7 microservices on a multi-tenant settlement platform, scaling throughput to 5M+ trades per day.
  - Designed a Spring Boot aggregation engine that folds high-volume trade streams into consolidated settlement instructions across configurable dimensions, cutting instruction volume by 70%.
  - Built an LLM-agent regression framework that generates and diagnoses multi-service test workflows, automating 300+ scenarios and cutting manual test effort 90%. Adopted by 30+ engineers across 5 teams.
---

## What the platform does

TODO: describe the settlement platform in a paragraph a non-specialist can follow. What is a
settlement instruction, why does volume matter, what breaks when it goes wrong.

## Launching a new business line

TODO: the 7 microservices, what "production readiness" meant concretely, what you owned versus
what you influenced, and the hardest design call you had to make.

## The aggregation engine

TODO: why 70% fewer instructions matters downstream. What the configurable dimensions are, and
what made the correct grouping non-obvious.

## LLM agents for regression testing

TODO: the most interesting thing here. What the agent actually does, why a generated test suite
beats a handwritten one for multi-service workflows, where it fails, and how you got 30+ engineers
on 5 teams to trust it.

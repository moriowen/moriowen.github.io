---
title: JP Morgan Chase
subtitle: Mumbai, India
meta: Jan 2026 - Jul 2026
order: 1
summary: >-
  Took a new business line to production across 7 microservices on the settlement platform, at 5M+
  trades per day. Also built LLM agent tooling for the SDLC: a pipeline that turns Jira tickets
  into reviewable PRs, and a regression framework now used by 30+ engineers on 5 teams.
roles:
  - title: Software Engineer II (Associate)
    when: Jan 2026 - Jul 2026
    where: Mumbai
    bullets:
      - Owned cross-service design and production readiness for a new business line across 7 microservices on a multi-tenant settlement platform, scaling throughput to 5M+ trades per day.
      - Built an agentic SDLC pipeline that autonomously translated Jira requirements into code changes across a multi-service architecture, reproduced issues with local infrastructure, validated via automated tests, and raised developer-ready PRs for review, with 75% PRs merged with minimal edits.
      - Built a regression framework using LLM agents that generates and diagnoses multi-service test workflows, automating 300+ scenarios and cutting manual test effort by 90%; adopted by 30+ engineers across 5 teams.
      - Designed an aggregation engine in Spring Boot reducing high-volume trade streams into consolidated settlement instructions across configurable dimensions, cutting down instruction volume by 70%.
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

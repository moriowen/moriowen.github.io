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

A trade is agreed in seconds, but the securities and cash change hands later, at settlement. In
between, the firm works out what it owes and is owed, tells the market, and checks that its version
matches the counterparty's. The message that tells the market is a settlement instruction, often a
SWIFT message, and each market sets a deadline for receiving it. An instruction that is late or
wrong means the trade does not settle on time.

The platform I worked on is a set of services along that path. One owns each trade's state until it
settles and groups trades into instructions. One sends instructions out to the market, one handles
the messages that come back in, and a datastore pulls all of it into one searchable view.

TODO: why volume matters, and what a failed settlement costs.

## Launching a new business line

Seven microservices on a multi-tenant platform, scaled to 5M+ trades per day.

The platform is shared by several business lines, so every change for the new flow also had to
leave the existing flows working.

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

The engine lives in the service that owns trade state. Different business flows group trades
differently, so the grouping is configuration rather than code: each flow names the combination of
business dimensions its trades are netted on, and the engine emits one consolidated instruction per
group for downstream processing.

TODO: why 70% fewer instructions matters downstream, what the dimensions are, and why the correct
grouping was not obvious.

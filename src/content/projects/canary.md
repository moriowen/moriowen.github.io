---
title: Canary
meta: Python, scikit-learn
order: 1
summary: >-
  Predicts whether a coding agent's run is going to fail from the first few steps of execution, so
  the doomed runs can be stopped early. Cuts agent compute by 25% for a one-point drop in solve
  rate, at 0.80 PR-AUC on a task-controlled evaluation.
bullets:
  - Cut coding-agent compute by 25% with a one-point drop in solve rate by predicting run failure from the first few steps of execution.
  - Built supervised models over 80k coding-agent trajectories from Agent SWE Bench to predict failure early, reaching 0.80 PR-AUC on a task-controlled evaluation.
  - Combined supervised prediction with unsupervised clustering to identify recurring failure modes across 59k failed runs, explaining why agents fail and when one should continue or stop.
---

## The bet

A coding agent that is going to fail usually starts failing early. If that is true, the tokens
spent on the back half of a doomed run are wasted, and a cheap classifier watching the opening
steps can reclaim them.

The trade the numbers describe: 25% less compute for one point of solve rate.

TODO: say plainly whether that trade is worth taking, and for whom. It reads differently for a
research benchmark than for someone paying per token in production.

## The data

80k trajectories from Agent SWE Bench, 59k of them failures.

TODO: what a trajectory actually contains, which prefix of it the model is allowed to see, and how
you chose that cutoff. The prefix length is the whole design.

## Predicting failure

Supervised models over trajectory prefixes, 0.80 PR-AUC on a task-controlled evaluation.

TODO: task-controlled is the important word and nobody will know what it means. Explain what
leaks if you do not control for task, and how much the number drops when you do not.

TODO: what the features are, and which ones carry the signal. If the model is mostly reading
"the agent is thrashing on the same file", say so.

## Why agents fail

Unsupervised clustering over the 59k failed runs to find recurring failure modes.

TODO: the most interesting section. Name the clusters. Which failure modes are recoverable and
which are terminal, and whether the classifier is really just detecting the terminal ones.

## Stopping rule

TODO: prediction is not the product, the stop-or-continue decision is. What threshold you picked,
what it costs to be wrong in each direction, and whether a killed run should be retried or
abandoned.

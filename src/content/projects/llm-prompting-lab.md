---
title: LLM Prompting Lab
meta: Ollama, Python
order: 2
summary: >-
  Benchmarks seven open-weight models on two tasks with checkable answers, character reversal and
  decimal division, across eleven temperatures and four prompting strategies. 14,935 graded trials,
  browsable down to the individual response.
external:
  - label: Live
    href: https://llm-prompting-lab.vercel.app/
bullets:
  - Ran 14,935 graded trials over seven open-weight models from 1.54B to 32.8B parameters, self-hosted through Ollama.
  - Graded against ground truth computed independently in Python with decimal.Decimal and fractions.Fraction, so accuracy is checked rather than judged.
  - Built an explorer that drills from aggregate accuracy down to raw model output, plus an error taxonomy separating wrong digits, rounding, and precision on division from character, length, and ordering errors on reversal.
---

## Why these two tasks

Most prompting advice gets argued over tasks where the answer is a matter of taste. Reversing a
string and dividing two decimals are not like that. There is one right answer, you can compute it
yourself, and grading needs no model in the loop, so temperature, model size, and prompting
strategy can be measured rather than debated.

## The grid

Seven models, 1.54B to 32.8B parameters, all self-hosted through Ollama with the CPU or GPU
backend recorded per run. Eleven temperature settings. Four prompting approaches: zero-shot,
few-shot, chain-of-thought, and verbose variants. 14,935 trials in total, each graded against
ground truth computed in Python.

## What came out of it

Temperature barely moves accuracy. Scaling behaves differently per task: division shows a
threshold, where models below a certain size mostly fail and models above it mostly do not, while
reversal shows no such jump. Prompting effects are model-specific, so a strategy that helps one
model can do nothing for the next one.

The item-level numbers are the part I keep coming back to. On reversal, two strings account for a
model's entire score. Aggregate accuracy over a small item set turns out to be mostly a statement
about which items you picked.

## The explorer

A single accuracy number would have hidden that, so the site keeps every layer: accuracy by
condition, error breakdowns by type, per-query performance, and the raw output for any individual
trial.

TODO: name the seven models and the exact query sets. Anyone reading the numbers should be able to
rerun them.

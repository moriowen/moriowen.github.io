---
title: Canary
meta: Python, PyTorch, LightGBM, vLLM
featured: true
order: 3
summary: >-
  A monitor that watches an AI coding agent while it works and stops runs that are heading for
  failure. On 16,140 held-out SWE-agent runs it cuts agent compute by 46% while stopping 2% of the
  runs that would have succeeded, against 25% for the best fixed turn limit.
external:
  - label: Code
    href: https://github.com/moriowen/canary
bullets:
  - Built a failure monitor for AI coding agents that cuts compute by 46% on 16,140 held-out SWE-agent runs while stopping only 2% of the runs that would have succeeded, against 25% for the best fixed turn limit.
  - Parsed 147k trajectories from two agent frameworks (SWE-agent and OpenHands) into one action schema, and trained logistic regression, LightGBM, a within-issue LightGBM ranker and a GRU on Georgia Tech's PACE cluster.
  - Measured how much early failure prediction is really task difficulty, AUROC 0.70 across all runs at turn 5 against 0.54 between attempts at the same issue, after finding and removing issue-level features that let models memorise per-issue solve rates.
---

<div class="glance">
<p class="glance-label">At a glance</p>
<dl>
<dt>Problem</dt>
<dd>Most AI coding-agent runs fail, and three quarters of all runs finish normally, submit a patch, and still fail. You only find out at the end, after paying for every turn.</dd>
<dt>Approach</dt>
<dd>After every turn, a model reads what the agent has done so far and estimates the chance the run ends in a fix. Below a threshold chosen for a fixed loss budget, the run is stopped and its compute goes elsewhere.</dd>
<dt>Setup</dt>
<dd>80,036 SWE-agent runs (Llama 8B, 70B and 405B) on 3,591 GitHub issues, and 67,074 OpenHands runs. Splits are by issue. Models trained on PACE ICE (A100, L40S, H100).</dd>
<dt>Headline</dt>
<dd>A GRU monitor saves 46.5% of context-token compute at 2% of successful runs lost, and 60.3% at 5%. The best fixed turn limit saves 24.6% and 39.6%.</dd>
<dt>Status</dt>
<dd>Fall 2026, in progress. The monitors, the evaluation and the cross-agent transfer test have run. A fine-tuned ModernBERT model and an LLM-built failure taxonomy are running.</dd>
</dl>
</div>

## The problem

An AI coding agent gets a GitHub issue and works in a loop: it thinks, runs a command, reads the
output, and goes again until it submits a patch. The repository's tests decide whether the patch
fixed anything.

In the public SWE-agent dataset I used, 16.7% of runs succeed. 74.8% of all runs exit normally,
submit a patch, and fail anyway, and the exit status for every one of them is `submitted`. Failed
runs also tend to be the long ones, and late turns are the expensive ones, because each step
re-reads the whole transcript so far. The usual guard is a fixed turn limit, which cuts slow
successes along with the failures.

## What the monitor sees

I converted both agent frameworks into one record per action: the kind of action (view, search,
edit, run, test, submit), the file it touched and whether that file is source, a test, or a
scratch reproduction script, and what came back: tracebacks, rejected edits, missing commands,
non-zero exit codes, and test pass and fail counts. SWE-agent and OpenHands look nothing alike on
the wire, but both reduce to the same loop.

From the first k turns the models get counts and rates of all of that, how often the agent repeats
a command, when it first edits a source file, whether it reran its reproduction after editing, and
how its reasoning reads. A run only gets a prediction at turn k if it is still going at turn k. The
exit status, the patch and the test logs are used to label runs and nothing else.

## Keeping the evaluation honest

The SWE-agent dataset has about 22 attempts per issue, and 77% of issues are never solved by any
attempt. That creates an easy way to look good: learn which issues are hopeless. A model that does
this fires at turn 0 and never changes its mind, which is useless for deciding when to stop a run.

Three things guard against it. Every attempt at an issue sits in the same train, validation or
test split. Each model is scored twice, over all test runs and only on pairs of attempts at the
same issue where one succeeded and one failed, which holds difficulty fixed. And the models get no
issue-level features. My first LightGBM leaned hardest on the issue's length and line count, which
are identical across an issue's attempts and work as an ID. Removing them raised held-out AUROC at
turn 5 from 0.665 to 0.699.

## Results

On the 16,140 SWE-agent test runs (718 issues), the question is how much compute a monitor saves
for a given share of successful runs it is allowed to stop.

| Monitor | Compute saved, 2% of successes lost | 5% lost | 10% lost |
|---|---:|---:|---:|
| GRU over per-turn signals | 46.5% | 60.3% | 66.3% |
| LightGBM on prefix features | 40.9% | 51.4% | 64.2% |
| Logistic regression | 34.8% | 50.6% | 63.0% |
| Rule: fixed turn limit | 24.6% | 39.6% | 64.0% |
| Rule: stop after N errors in a row | 19.6% | 25.8% | 36.1% |

<img src="/projects/figures/canary-policy.png" alt="Line chart of compute saved (percent of context tokens) against successful runs killed (percent, 0 to 20). The GRU monitor is highest throughout, saving about 46% at 2% and 60% at 5%. LightGBM and logistic regression sit below it. The fixed turn limit starts lower but meets the learned monitors near 10%. The consecutive-errors rule and an issue-text-only model are well below." width="992" height="704" loading="lazy" />

Losing 2% of successes costs a third of a point of solve rate on this test set (16.3% to 15.9%).
The learned monitors win clearly at small loss budgets. At 10% a fixed turn limit catches up,
because on this agent long runs almost always fail.

## How much of it is task difficulty

Over all test runs, LightGBM reaches AUROC 0.70 by turn 5. Between attempts at the same issue it
is 0.54, barely above chance. The run-level signal builds slowly, and the best monitors reach about
0.70 on same-issue pairs by turn 20. The gap between the two views is how much of early failure
prediction is really "this issue is hard".

<img src="/projects/figures/canary-auroc.png" alt="Two line charts of AUROC against turns observed, 0 to 30. Left, across all test runs: the monitors rise from about 0.51 at turn 0 to about 0.70 by turn 5, with a non-deployable task-difficulty oracle flat near 0.94. Right, between attempts at the same issue: the monitors start near 0.51 and climb slowly to between 0.67 and 0.77 by turn 30, with a ranker trained only on same-issue pairs near the top." width="1760" height="736" loading="lazy" />

The strongest single feature is how often the agent hedges in its own reasoning, words like
"seems", "might" and "perhaps". Next come how soon it first edits a source file, how long its
reasoning runs, and how large its edits are.

## A stronger agent, and transfer

On OpenHands (47.9% of runs solved, median 61 turns against 17), the same approach saves 11% of
compute at 5% loss, and a fixed turn limit saves nothing because successful runs are long too.
Checked one at a time, none of the behaviour features separates attempts at the same issue, even 30
turns in.

Transfer between the two frameworks only works one way. A monitor trained on OpenHands and run on
SWE-agent saves 41.7% at 5% loss, against 51.7% for one trained on SWE-agent with the same
features. Trained on SWE-agent and run on OpenHands, it is at chance. Re-expressing each feature as
a percentile within its own framework's runs did not help.

## Why agents fail

TODO: an LLM (Qwen3-30B-A3B through vLLM) is reading each quiet failure with hindsight (transcript,
final patch, still-failing tests) and writing a diagnosis. The diagnoses get clustered and named,
then joined back to the monitor to see which kinds of failure show up early and which only at the
end. Results go here when the run finishes.

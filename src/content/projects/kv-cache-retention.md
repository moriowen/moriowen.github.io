---
title: "Lost in Compression: An Empirical Analysis of KV-Cache Retention and Failure Modes"
meta: PyTorch, Transformers, KVCache-Factory, Slurm
featured: true
cover:
  src: /projects/covers/kv-cache-retention.png
  alt: "Cover: a grid of prompt tokens per attention head, with only a few kept in each row and the rest dimmed"
order: 2
summary: >-
  Four KV-cache compression methods on Llama-3-8B, each held to the same 16 MiB of prompt cache
  (10 to 63× less than the full cache), with a log of every position each layer and head kept.
  All four land within 3 F1 of the full cache, and no ranking survives a paired bootstrap. Next: a
  budget sweep, stress tests and cache interventions to find out why answers fail and which method
  to use when.
bullets:
  - Compared SnapKV, PyramidKV, Ada-SnapKV and HeadKV-R2 against the uncompressed cache on Llama-3-8B-Instruct and LongBench multifieldqa_en, with each method calibrated so its measured prompt K/V is 16 MiB ±0.5% rather than set to the same nominal capacity.
  - Recorded the original prompt positions kept by every layer and KV head for 525 answers, and caught that the saved source offsets were zero-width for 355,150 of 436,774 tokens. Recovered the alignment from the raw byte-level tokens and validated it on all 92 prompts before using it.
  - Reviewed HeadKV's failures case by case and found two patterns, evidence dropped from the cache and evidence kept but not used, then wrote a five-experiment plan with decision rules fixed before any new run.
---

<figure class="system-flow">
<p class="system-flow-label">Compare compression at equal memory</p>
<ol aria-label="Compare compression at equal memory">
<li><strong>Fixed workload</strong><span>Llama-3-8B and LongBench questions.</span></li>
<li><strong>Calibrate cache size</strong><span>Give each compression method 16 MiB of prompt KV.</span></li>
<li><strong>Record retention</strong><span>Log the positions kept by each layer and head.</span></li>
<li><strong>Inspect failures</strong><span>Compare answer F1 and retained evidence.</span></li>
</ol>
<figcaption>The completed run is observational. Planned cache interventions are separate follow-up work.</figcaption>
</figure>

<div class="glance">
<p class="glance-label">At a glance</p>
<dl>
<dt>Problem</dt>
<dd>The KV cache grows with every prompt token and limits how many users one GPU can serve. Compression methods keep a small part of it and drop the rest. They differ in how they split the budget across layers and heads, and it is not clear which split loses the least, or why a compressed answer goes wrong.</dd>
<dt>Approach</dt>
<dd>Hold the model, inputs, decoding and measured cache size fixed, change only the compression method, and log which prompt positions each layer and head kept. Then read the failures against the source text, and plan interventions on the cache to test cause.</dd>
<dt>Setup</dt>
<dd>Llama-3-8B-Instruct in bf16 on one A100 80GB (Georgia Tech ICE cluster). LongBench multifieldqa_en, 92 questions of 1,345 to 8,079 tokens. Pinned KVCache-Factory implementations. Greedy decoding, at most 64 new tokens.</dd>
<dt>Headline</dt>
<dd>At 16 MiB the four methods score 44.4 to 46.4 F1 against 47.2 for the full cache, and every 95% interval of the difference includes zero. Longer prompts lose more: on the longer half, PyramidKV falls to 37.4 against 42.8.</dd>
<dt>Status</dt>
<dd>Fall 2026, team project for CS 6220 at Georgia Tech. The 16 MiB run is complete and audited, and the HeadKV failure review is done. Human labels for the other methods and all five follow-up experiments have not run.</dd>
</dl>
</div>

## The problem

When a language model reads a prompt, it stores a key and a value vector for every token, in every
layer. For Llama-3-8B that is 32 layers × 8 KV heads × 128 dimensions × 2 (K and V) × 2 bytes,
or 0.125 MiB per token. A 5,000-token prompt costs about 625 MiB of cache for one user.

Eviction methods cut this down after prefill. Each layer scores the prompt tokens, keeps the top
rows per head, and drops the rest for the rest of the request. The methods agree on scoring by
attention from the end of the prompt. They disagree on where the budget goes:

| Method | How it splits the budget |
|---|---|
| [SnapKV](https://arxiv.org/abs/2404.14469) | The same number of positions in every layer and head |
| [PyramidKV](https://arxiv.org/abs/2406.02069) | More positions in early layers, fewer in later ones |
| [Ada-SnapKV](https://arxiv.org/abs/2407.11550) | Moves capacity between heads within a layer, per input |
| [HeadKV-R2](https://arxiv.org/abs/2410.19258) | A fixed per-head table from retrieval and reasoning importance scores, the same for every input |

Each paper reports its own setup. We wanted one comparison where the only thing that changes is
the method, and where a failure can be traced to what the cache did or did not keep.

## Matching the budget

Equal nominal settings do not give equal memory across these implementations. So each method was
calibrated until its measured prompt K/V, over all layers and heads and including the 8-token
recent window, was 16,777,216 bytes ±0.5%. That is the size of 128 tokens of full cache, and 2 to
10% of each prompt. The capacity settings that hit it were 128 for SnapKV, 117 for PyramidKV, 128
for Ada-SnapKV and 120 for HeadKV.

Everything else is fixed: the model revision, the 92 tokenized inputs (questions whose prompt plus
64 output tokens fit in 8,192, with no truncation), the official LongBench prompt, greedy decoding,
batch size one, and the runtime. The methods do still use different attention code paths, so a
score gap is not purely the effect of the allocation rule.

The run produced 525 answers in one Slurm batch: 50 calibration answers, 15 repeats that had to
reproduce exactly, and 460 main answers. Inside the pinned implementation it also logged, for every
answer, which original prompt positions each layer and head kept, plus selection scores and
allocation details. Offline audits checked file integrity, trace bounds and per-head lengths, and
the instrumented answers matched an earlier untraced run token for token.

## Results at 16 MiB

Official LongBench QA F1 on the 92 questions. F1 is word overlap with the reference answer, so it
is a score, not a correctness rate. Intervals are a paired bootstrap over questions.

| Method | F1 | Change vs. full cache | 95% interval | Same text as full cache |
|---|---:|---:|---|---:|
| Full cache (168 to 1,010 MiB) | 47.18 | | | 92 / 92 |
| Ada-SnapKV | 46.39 | −0.79 | −4.9 to +3.5 | 46 / 92 |
| SnapKV | 46.21 | −0.97 | −4.8 to +2.9 | 49 / 92 |
| HeadKV-R2 | 46.00 | −1.18 | −4.9 to +2.4 | 51 / 92 |
| PyramidKV | 44.39 | −2.79 | −6.3 to +0.4 | 49 / 92 |

Every interval includes zero, so this run cannot rank the methods. About half of each method's
answers are word for word what the full cache wrote.

Prompt length is where they separate. On the shorter 46 questions (1,345 to 4,725 tokens) every
method is within about 2 points of the full cache's 51.5, and HeadKV is above it at 53.2. On the
longer 46:

<div class="chart">
<p class="chart-title">F1 on the longer half of questions (4,726 to 8,079 tokens)</p>
<div class="bar"><span class="bar-label">Full cache</span><span class="bar-track"><span class="bar-fill" style="--w:100%"></span></span><span class="bar-value">42.8</span></div>
<div class="bar"><span class="bar-label">SnapKV</span><span class="bar-track"><span class="bar-fill" style="--w:97.9%"></span></span><span class="bar-value">41.9</span></div>
<div class="bar"><span class="bar-label">Ada-SnapKV</span><span class="bar-track"><span class="bar-fill" style="--w:95.1%"></span></span><span class="bar-value">40.7</span></div>
<div class="bar"><span class="bar-label">HeadKV-R2</span><span class="bar-track"><span class="bar-fill" style="--w:90.7%"></span></span><span class="bar-value">38.8</span></div>
<div class="bar dim"><span class="bar-label">PyramidKV</span><span class="bar-track"><span class="bar-fill" style="--w:87.4%"></span></span><span class="bar-value">37.4</span></div>
<p class="chart-note">Bar length relative to the full cache. Each half has only 46 questions, so this is a lead, not a result.</p>
</div>

## Two ways a compressed answer fails

The position logs make it possible to ask, for a wrong answer, whether the evidence was in the
cache at all. Two cases show the two answers to that question.

**Evidence dropped (#78).** The question asks for a list of dataset names. The full cache answers
`URPC2017, URPC2018, URPC2019, URPC2020_ZJ, URPC2020_DL, and UDD`. SnapKV, PyramidKV and Ada-SnapKV
all drop the `_ZJ` and `_DL` suffixes, and SnapKV and Ada-SnapKV continue the pattern into years
that the document never mentions (`URPC2021`, `URPC2022`, ...). The `DL` token appears four times in
the prompt. SnapKV, PyramidKV and Ada-SnapKV kept it in 0% of layer-head pairs, and HeadKV in 0.3%.

**Evidence kept, not used (#50).** The question asks for one of an author's papers in the Journal
of Controlled Release. HeadKV kept intact copies of two correct title and journal spans in several
layer-head pairs, and still wrote a title that is not in the document, with hemophilia A changed
to B and a different delivery mechanism.

The first kind points at the selection rule. The second points somewhere else, perhaps at how the
kept evidence is spread across heads. Neither is proven yet: a dropped token alongside a wrong
answer is a correlation.

## A bug in our own logs

While aligning kept positions to source text for the case review, we found that the saved
token-to-character offsets were zero-width for 355,150 of 436,774 prompt tokens. Any analysis that
used them would have undercounted the evidence a method kept. The audits had checked that offsets
were in bounds and consistent, not that they covered the text. The raw token IDs, kept indices,
answers and scores were all intact. We rebuilt the alignment from the saved byte-level token pieces,
validated it independently on all 92 prompts, including multi-byte UTF-8 characters, and use it for
every source-based number on this page. The original run files stay unchanged.

## HeadKV, case by case

I reviewed HeadKV's five candidate failures against the source documents. HeadKV changed 41 of 92
answers, with lower F1 on 16 and higher F1 on 18. Of roughly 42 questions the full cache probably
got right (F1 of 0.5 or more), HeadKV likely got 6 to 8 wrong. Only a human check of the 17
differing answers can confirm that count.

Its fixed table is very uneven. Rows per head range from 10 to 736 with a median of 38, and 37% of
heads keep 20 rows or fewer. In both detailed cases, every kept copy of the evidence sat in a few
large-budget heads in the middle layers. Its failures cluster on exact details (a `DL` suffix, part
of an exponent in a copied formula) and on answers that must keep a condition, such as a quantity
that rises and then declines. Within this run, HeadKV fits short-answer lookup on moderate-length
prompts when memory is the constraint, and needs a manual check when exact strings matter.

## What this run cannot say

- Which method is best. The intervals overlap.
- That a dropped token caused a wrong answer.
- Whether any answer is right for a human reader. Labels for SnapKV, PyramidKV and Ada-SnapKV are
  still pending.
- Anything about speed or users per GPU. Timings include tracing overhead, and every request ran
  alone.

## Next: five experiments

The 16 MiB run measures one side of the trade-off, at one budget, on one task that suits these
methods. Each experiment below closes one gap, and each new GPU run gets its own experiment ID so
the completed run stays untouched.

| | Question | What we do | Result |
|---|---|---|---|
| 1. Failure labels | When a compressed answer is wrong, what kind of wrong is it, and was the evidence dropped? | A person labels every answer that differs from the full cache (about 41 to 46 per method), then checks the kept positions for each real failure. No GPU. | A count per method of real failures, split into evidence dropped and evidence kept |
| 2. Budget sweep | At what budget does each method break? | Run every method at 50, 25, 10, 5, 2.5 and 1% of the prompt, byte-matched to SnapKV at each level. For each question, find the smallest budget where the answer still matches the full cache. | F1 against budget per method, and what the memory-hungry questions share. About 2,200 answers. |
| 3. Stress tests | What kinds of input break each method? | Vary one assumption at a time: number of hidden facts (1 to 32), question before the document instead of after, multi-hop questions, near-duplicate names like case #78. Optionally RULER and LongBench hotpotqa and 2wikimqa. | For each method, which inputs break it and at what budget |
| 4. Evidence swap | Did the missing evidence cause the failure? | Rerun a failure, swap the evidence rows in for the lowest-scoring rows at the same 16 MiB, then repeat with random rows as a control. | Cause, for the 30 to 60 failures with literal evidence. Rescue by evidence and not by random rows means the drop caused the error. |
| 5. Users per GPU | What does compression buy? | 1 to 64+ concurrent requests on one GPU for the full cache and for SnapKV at a few budgets, including 256 to 512-token answers. | Throughput, time per output token, memory, and the most users that fit |

Experiment 5 matters because batch size one hides the gain. By a rough estimate for a
5,000-token prompt, compression saves about 4% of the bytes read per decode step at batch 1, and
about 70% at 64 users, because the 16 GB of weights are read once per step but every user's cache
is read too. The experiment replaces that estimate with a measurement. It first needs a check that
the Factory code supports batches for these methods.

The stress tests target the one assumption all four methods share: that the end of the prompt,
where the question sits, points at the tokens worth keeping. Putting the question first, or asking
for a second fact that the question never names, breaks it on purpose.

## How the recommendation gets decided

The rules are written down before the new results exist, so the conclusion cannot be fitted to
the data afterwards.

1. Method A beats method B at a budget only if the paired 95% interval of A minus B excludes zero.
2. If no method wins on quality, they are tied, and the choice goes to serving gain, then to
   engine fit.
3. Each workload is reported on its own (single-fact QA, multi-hop, each stress test), never
   averaged together.

Engine fit counts because SnapKV keeps the same number of rows in every head, which maps onto paged
memory in engines like vLLM. PyramidKV varies by layer, and Ada-SnapKV and HeadKV vary by head,
which needs new memory handling. The output is a table of which method to use by workload and
budget, with the evidence behind each entry. A tie is an acceptable answer: "above 10% budget the
methods are equal, so use SnapKV because it is simplest" would be a clear recommendation.

## Limitations

- **One model, one task.** Llama-3-8B-Instruct on LongBench multifieldqa_en.
- **Not paper reproductions.** These are pinned KVCache-Factory implementations, and their
  attention code paths differ, so score gaps are not allocation-only effects.
- **92 questions.** They include the 10 calibration questions, some share source documents, and
  58 of the 150 source questions were excluded by the length rule.
- **F1 is word overlap.** A correct paraphrase can score low, and a missing qualifier can score
  high. Human labels are complete only for HeadKV's five cases.

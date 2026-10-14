---
title: Non-prefix KV Cache Reuse for Agent Memory
meta: PyTorch, Transformers, vLLM
featured: true
order: 1
summary: >-
  Caches each agent memory's KV once and reuses it wherever the memory lands in the prompt, which
  prefix caching cannot do. Served through unmodified vLLM it cut time to first token by up to
  2.28×, with four published KV correction methods compared on 1,986 LoCoMo questions.
external:
  - label: Code
    href: https://github.com/moriowen/kvreuse
bullets:
  - Built non-prefix KV reuse for a memory-augmented agent on Mistral-7B, with exact RoPE re-rotation of cached keys and a hand-written per-layer forward pass that matches Hugging Face to 4.6e-5 in max logit error.
  - Served reuse through vLLM's public KV connector API with no engine changes, cutting median time to first token from 60.6 ms to 26.6 ms (2.28×) at ten retrieved memories, where prefix caching managed 1.10×.
  - Compared four correction methods (re-positioning, EPIC, CacheBlend, AgentKVShift, the last reimplemented from its paper) on all 1,986 LoCoMo questions under one recompute-budget formula, mapping how much answer quality each recovers per unit of recompute.
---

<div class="glance">
<p class="glance-label">At a glance</p>
<dl>
<dt>Problem</dt>
<dd>An agent with long-term memory retrieves a different mix of memories for every question, in a different order. The serving engine's prefix cache misses them, so the same text gets prefilled again and again.</dd>
<dt>Approach</dt>
<dd>Cache each memory chunk's KV once, keyed by its tokens. Load it wherever the chunk appears, fix its position exactly with a RoPE rotation, and correct the remaining error by recomputing a small set of tokens.</dd>
<dt>Setup</dt>
<dd>Mistral-7B-Instruct-v0.3 on an H100. LoCoMo long-conversation benchmark (10 conversations, 17K to 31K tokens, 1,986 questions). BM25 top-10 retrieval. vLLM 0.27.1.</dd>
<dt>Headline</dt>
<dd>Served through vLLM, time to first token fell 2.28× at ten retrieved memories, and throughput rose 52% when 90% of requests reuse memories. Uncorrected reuse also halves answer quality, which is what the correction methods are for.</dd>
<dt>Status</dt>
<dd>Fall 2026, in progress. The correctness gate, the quality sweep, the prefill-time sweep, and both serving benchmarks have run. The end-to-end check that vLLM's output matches the reference has not.</dd>
</dl>
</div>

## The problem

A chat agent that talks with someone for months cannot fit the whole history in its context
window. Systems like MemGPT and A-Mem store the conversation as memory entries instead, and for each
new question a retriever picks the few most relevant entries and pastes them into the prompt.

Before the model writes its first token it runs **prefill**, one pass over every prompt token that
produces a key and a value vector per token per layer: the KV cache. Prefill cost grows with prompt
length and dominates **time to first token (TTFT)**. For Mistral-7B the cache is 128 KB per token.

Serving engines already skip some of that work. vLLM's prefix caching and SGLang's RadixAttention
reuse KV between requests, but only when the requests start with identical tokens. Memory
retrieval breaks that condition constantly:

<figure>
<img src="/projects/figures/kvreuse-problem.jpg" alt="Two prompts: question 1 is System, Memory A, B, C, Q1; question 2 is System, Memory C, A, D, Q2. Only the system prompt hits the prefix cache; memories C and A were already computed for question 1 but are prefilled again because they moved." width="1400" height="788" loading="lazy" />
<figcaption>Question 2 needs memories C and A, computed seconds earlier for question 1. They moved, so the prefix cache misses them.</figcaption>
</figure>

## The approach

<ol class="flow">
<li><b>Chunk.</b> Whole dialogue turns from one session, packed to about 256 tokens and never split mid-turn.</li>
<li><b>Prefill alone.</b> The first time a chunk is retrieved, prefill it by itself and store its KV under a hash of its tokens.</li>
<li><b>Load.</b> Later prompts that contain the chunk fetch the stored KV, wherever the chunk lands.</li>
<li><b>Re-rotate.</b> Move the cached keys to their new position with one extra RoPE rotation.</li>
<li><b>Correct.</b> Recompute a few tokens against the assembled cache. The question at the end is always computed fresh.</li>
</ol>

Reused KV is wrong in two different ways, and they need different fixes.

| | Error | Fix |
|---|---|---|
| **Position** | Mistral uses rotary position embeddings, so a cached key encodes where its token sat when it was cached. | Exact. Rotations compose, so one extra rotation by the position difference moves a key to its new place. Done in fp32 and cast once. |
| **Context** | A chunk cached alone never attended to the chunks now in front of it, so its KV above the first layer is slightly off. | Approximate. No rotation fixes this; the only remedy is recomputing some tokens against the full cache. |

Which tokens to recompute is the research question. Four published answers are plugged into the
same per-layer recompute loop and charged by the same budget formula:

| Method | Recomputes | Bets that the error... |
|---|---|---|
| Re-positioning only (baseline) | nothing | is small enough to ignore |
| Boundary ([EPIC](https://arxiv.org/abs/2410.15332)) | the first k tokens of each chunk | sits at chunk starts, where chunks cached alone form attention sinks |
| Dynamic selection ([CacheBlend](https://arxiv.org/abs/2405.16444)) | the tokens that deviate most at an early layer | is concentrated in a few tokens |
| Offset correction ([AgentKVShift](https://arxiv.org/abs/2607.21604)) | a few probe tokens, then their mean shift applied to the rest | is a shared shift across each chunk |

The correction algorithms come from prior work. The contribution is engineering and evaluation:
all four on one conversational-memory workload under one cost accounting, a reimplementation of
AgentKVShift (which has no public code), and non-prefix reuse served through vLLM's public KV
connector API with no changes to the engine.

## Is it correct?

Every later number depends on this, so the experiment chain stops if it fails. A hand-written
per-layer forward pass replaces the Hugging Face model call, and on 20 real LoCoMo prompts in fp32
it has to match the reference wherever an exact match is expected:

| Check | Worst max-abs logit error | Gate |
|---|---|---|
| Hand-written forward vs. Hugging Face | 4.6e-5 | 1e-3 |
| Recomputing 100% of tokens vs. full prefill | 7.3e-5 | 1e-3 |
| Chunk reused exactly where it was cached vs. full prefill | 4.2e-5 | 1e-3 |

All three pass by more than 13×. The bf16 noise floor, used to read the later runs, is a mean KL of
6.4e-4 on the first answer token with 100% top-1 agreement.

## How much quality does each method keep?

LoCoMo F1 on all 1,986 questions, against full prefill of the same retrieved prompt (0.319). The
whole 17K to 31K-token conversation, with no retrieval, scores 0.326, so retrieval itself costs
almost nothing.

<figure>
<img src="/projects/figures/kvreuse-quality-vs-budget.png" alt="Line chart of LoCoMo F1 against recompute budget from 0 to 1. Re-position only sits at 0.152. EPIC rises to 0.236 at 28% budget, CacheBlend to 0.284 at 63%, AgentKVShift to 0.302 at 71%, just inside the band within 0.02 of full prefill at 0.319." width="1400" height="880" loading="lazy" />
<figcaption>Answer quality against recompute budget. AgentKVShift leads at nearly every budget; only its largest setting reaches the target band within 0.02 F1 of full prefill.</figcaption>
</figure>

<div class="chart">
<p class="chart-title">LoCoMo F1 at roughly a fifth of tokens recomputed</p>
<div class="bar"><span class="bar-label">Full prefill (reference)</span><span class="bar-track"><span class="bar-fill" style="--w:100%"></span></span><span class="bar-value">0.319</span></div>
<div class="bar"><span class="bar-label">CacheBlend, 20% budget</span><span class="bar-track"><span class="bar-fill" style="--w:70.8%"></span></span><span class="bar-value">0.226</span></div>
<div class="bar"><span class="bar-label">AgentKVShift, 18% budget</span><span class="bar-track"><span class="bar-fill" style="--w:70.5%"></span></span><span class="bar-value">0.225</span></div>
<div class="bar"><span class="bar-label">EPIC, 14% budget</span><span class="bar-track"><span class="bar-fill" style="--w:63.3%"></span></span><span class="bar-value">0.202</span></div>
<div class="bar dim"><span class="bar-label">Re-positioning only, 0%</span><span class="bar-track"><span class="bar-fill" style="--w:47.6%"></span></span><span class="bar-value">0.152</span></div>
<p class="chart-note">Bar length relative to full prefill. Budget is the charged fraction of reusable token-layers.</p>
</div>

- **Uncorrected reuse loses half the quality.** F1 drops from 0.319 to 0.152. Temporal questions
  suffer most (0.207 to 0.052): a chunk cached alone has not linked its dates to the other chunks,
  and in several cases the model answers that the conversation does not say.
- **Quality comes back slowly.** At 10 to 20% budget the methods recover between a fifth and a
  little under half of the lost F1. AgentKVShift reaches 0.302, within 0.02 of full prefill, only at 70% budget.
- **The papers' headline claim does not hold here.** The target was AgentKVShift within 0.02 F1 at
  10 to 15% budget. At 12% it scores 0.210, 0.109 below full prefill. This setup uses plain BM25
  conversation chunks rather than AgentKVShift's metadata-rich memory system, which is one likely
  reason, and the gap is reported as found.

## How much prefill does reuse remove?

Median prefill time on 300 questions at ten retrieved chunks (about 2.4K prompt tokens), H100,
bf16.

<div class="chart">
<p class="chart-title">Median prefill time, ten retrieved chunks (ms, lower is better)</p>
<div class="bar"><span class="bar-label">Re-positioning only</span><span class="bar-track"><span class="bar-fill" style="--w:29.2%"></span></span><span class="bar-value">29.6</span></div>
<div class="bar"><span class="bar-label">CacheBlend, 15%</span><span class="bar-track"><span class="bar-fill" style="--w:33.1%"></span></span><span class="bar-value">33.5</span></div>
<div class="bar"><span class="bar-label">Full prefill</span><span class="bar-track"><span class="bar-fill" style="--w:74.5%"></span></span><span class="bar-value">75.4</span></div>
<div class="bar dim"><span class="bar-label">AgentKVShift, 10%</span><span class="bar-track"><span class="bar-fill" style="--w:100%"></span></span><span class="bar-value">101.2</span></div>
<p class="chart-note">Scale 0 to 101 ms. Gray bar is slower than full prefill.</p>
</div>

Re-positioning is 2.5× faster than full prefill and CacheBlend 2.3×. The AgentKVShift
reimplementation is slower than full prefill: its probe passes add more than the recompute saves.
Re-positioning stays at about 29.5 ms from two chunks to ten, which shows the remaining cost is
fixed overhead. The hand-written layer loop launches about 1,500 small kernels per call, so CUDA
graphs or `torch.compile` are the obvious next step.

Getting clean timings took one detour. Profiling showed PyTorch choosing cuDNN's attention kernel,
which rebuilds its execution plan for every new sequence length. Every LoCoMo prompt has a new
length, so each call paid about 40 to 45 ms of planning. Excluding cuDNN removed it. Timings from
runs before that fix are discarded; their F1 scores are unaffected.

## Does it help in a real server?

The vLLM connector plugs into vLLM's public KV connector API, so the engine itself is unmodified.
That limits it to re-positioning: the correction methods recompute tokens inside the prompt at
every layer, which would need scheduler changes.

**Latency as more memories are retrieved.** Median TTFT, three repetitions of 199 requests each:

| Retrieved chunks | Full prefill | Prefix cache | Connector | Connector speedup |
|---|---|---|---|---|
| 2 | 24.3 ms | 17.4 ms | 17.5 ms | 1.39× |
| 4 | 31.1 ms | 26.5 ms | 19.8 ms | 1.57× |
| 6 | 40.5 ms | 35.3 ms | 22.0 ms | 1.84× |
| 8 | 50.3 ms | 45.5 ms | 24.1 ms | 2.08× |
| 10 | 60.6 ms | 55.2 ms | 26.6 ms | **2.28×** |

At ten chunks the connector serves 97% of prompt tokens from cache against 18% for the prefix
cache. The advantage grows with every chunk added, because the prefix cache can only ever match the
system prompt.

**When does reuse beat prefix caching?** A synthetic workload where memory popularity follows a
Zipf distribution, with the reuse rate swept from 0 to 90%:

<div class="chart">
<p class="chart-title">Throughput at 90% reuse (requests per second)</p>
<div class="bar"><span class="bar-label">Connector</span><span class="bar-track"><span class="bar-fill" style="--w:100%"></span></span><span class="bar-value">38.0</span></div>
<div class="bar"><span class="bar-label">Prefix cache</span><span class="bar-track"><span class="bar-fill" style="--w:75.4%"></span></span><span class="bar-value">28.7</span></div>
<div class="bar"><span class="bar-label">Full prefill</span><span class="bar-track"><span class="bar-fill" style="--w:65.9%"></span></span><span class="bar-value">25.0</span></div>
</div>

Up to half the requests reusing memories, all three are within a few percent of each other. At 75%
the connector pulls ahead (1.39× faster TTFT), and at 90% it is 1.73× faster TTFT with 52% more
throughput than full prefill, against 1.14× and 15% for the prefix cache. Reuse pays off once
memories repeat often, which is the regime a long-running agent lives in.

## The catch

The fast serving path is the low-quality one. The connector serves re-positioning only, and
re-positioning halves F1. The serving results show how much latency non-prefix reuse can remove;
the quality results show that keeping answers intact needs a correction method that a stock vLLM
cannot yet run. Closing that gap, cheaply and inside the engine, is the open problem.

## Limitations

- **The end-to-end match check has not run.** The experiment comparing vLLM's tokens and KV against
  the Transformers reference is written but not yet executed, so the serving and quality results
  have not been tied together.
- **One model, one benchmark.** Mistral-7B on LoCoMo only.
- **Absolute F1 is low.** Full prefill scores 0.319 against AgentKVShift's published 0.509. Their
  memory system adds generated metadata where this uses plain BM25 chunks, and answers in an early run
  averaged about 14 words for a "short phrase" prompt, which pulls token F1 down. Comparisons are made
  within this setup.
- **The serving workload is synthetic.** The reuse-rate sweep uses a Zipf memory pool, not real
  agent traces.
- **The AgentKVShift reimplementation is unoptimized**, so its prefill time says more about this
  implementation than about the method.

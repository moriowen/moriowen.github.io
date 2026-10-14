---
title: Finetuning Lab
meta: PyTorch, PEFT, TRL
featured: true
order: 2
summary: >-
  LoRA at nine ranks from 1 to 256, plus full fine-tuning, on Qwen2.5-1.5B with TruthfulQA, three
  seeds each. Every version lifts accuracy from 0.28 to about 0.45 and rank makes no measurable
  difference. A silent NaN gradient in fused attention first produced a convincing "higher rank is
  better" result, and the rerun made it disappear.
external:
  - label: Live
    href: https://finetuning-lab.vercel.app/
  - label: Code
    href: https://github.com/moriowen/finetuning-lab
bullets:
  - Fine-tuned Qwen2.5-1.5B-Instruct on TruthfulQA with LoRA at nine ranks, a fixed-α control, and a full fine-tune, three seeds each on an H100, lifting MC1 accuracy on 100 held-out questions from 0.28 to 0.45, significant on every seed under a paired McNemar test.
  - Showed rank does not matter at this data size. Accuracy is flat from r=1, with 0.07% of weights trainable, to r=256, while LoRA r=8 matches full fine-tuning at 6.6× less GPU memory and a 37 MB adapter instead of a 6.2 GB model.
  - Traced a fake "higher rank is better" trend to a NaN gradient in PyTorch's fused attention that silently cut runs short, then reran everything with standard attention and a non-finite guard.
---

<div class="glance">
<p class="glance-label">At a glance</p>
<dl>
<dt>Question</dt>
<dd>How much does LoRA rank matter when fine-tuning a small model on a small dataset, and what does full fine-tuning buy on top?</dd>
<dt>Setup</dt>
<dd>Qwen2.5-1.5B-Instruct on TruthfulQA (645 training, 72 validation, 100 test questions). LoRA at r = 1 to 256, a fixed-α control, and a full fine-tune. Three seeds each, one H100 per job.</dd>
<dt>Headline</dt>
<dd>Every fine-tuned model goes from 0.28 to about 0.45 MC1 accuracy. Rank 1 already gets 0.42. Full fine-tuning gets 0.47 at 6.6× the memory.</dd>
<dt>Takeaway</dt>
<dd>With this little data, the adapter is not the bottleneck, and most of what fine-tuning changes is how the model answers rather than what it knows.</dd>
</dl>
</div>

## The question

LoRA freezes a model's weights and trains two small matrices beside each layer. The rank r sets how
big those matrices are: rank 1 trains about 1.2M parameters here, rank 256 about 295M. Picking r is
usually a guess. This experiment sweeps it from 1 to 256 and puts a full fine-tune next to it, so
the answer comes from data rather than convention.

TruthfulQA fits the job. Each question comes with one true answer and several common
misconceptions, which tests whether fine-tuning moves a model away from popular falsehoods.

## Setup

<ol class="flow">
<li><b>Split</b> TruthfulQA's 817 questions (38 categories) once: 645 train, 72 validation, 100 test, stratified by category, with no question text in two sets.</li>
<li><b>Train</b> with TRL's SFTTrainer. Each example is the question with the dataset's best answer as the target; loss is on answer tokens only.</li>
<li><b>Sweep</b> LoRA (Hugging Face PEFT, all seven linear projections) at r = 1, 2, 4, 8, 16, 32, 64, 128, 256 with α = 2r, plus a fixed α = 16 control. Add a full fine-tune at learning rate 1e-5.</li>
<li><b>Stop early</b> on validation loss, checking every 20 steps with patience 2, and keep the best checkpoint.</li>
<li><b>Evaluate</b> MC1 on the 100 test questions, judged free-form answers, forgetting on MMLU and HellaSwag, latency, and memory.</li>
</ol>

**MC1** is TruthfulQA's own accuracy measure: the model scores every option by how likely it finds
that text as a reply, and it is right when the true option scores highest. With 100 test questions,
one model's accuracy has a standard error of about 5 points. Comparisons between models on the
same questions are tighter, because only the questions where they disagree count.

## Result: the gain is real

<div class="chart">
<p class="chart-title">MC1 accuracy on 100 held-out questions (mean of 3 seeds)</p>
<div class="bar"><span class="bar-label">Full fine-tune</span><span class="bar-track"><span class="bar-fill" style="--w:47.3%"></span></span><span class="bar-value">0.473</span></div>
<div class="bar"><span class="bar-label">LoRA r=8</span><span class="bar-track"><span class="bar-fill" style="--w:45%"></span></span><span class="bar-value">0.450</span></div>
<div class="bar"><span class="bar-label">LoRA r=64</span><span class="bar-track"><span class="bar-fill" style="--w:44.7%"></span></span><span class="bar-value">0.447</span></div>
<div class="bar"><span class="bar-label">LoRA r=1</span><span class="bar-track"><span class="bar-fill" style="--w:41.7%"></span></span><span class="bar-value">0.417</span></div>
<div class="bar dim"><span class="bar-label">Base model</span><span class="bar-track"><span class="bar-fill" style="--w:28%"></span></span><span class="bar-value">0.280</span></div>
<p class="chart-note">Scale 0 to 1. The base model is one deterministic run.</p>
</div>

Both models answer the same 100 questions, so the right test looks only at the questions where
they disagree (McNemar's test). Every fine-tuned run fixes far more than it breaks: the first r=8
seed fixes 21 questions and breaks none, and the full fine-tunes fix 17 to 25 while breaking 2 or
3. Every run is significant.

## Result: rank does not matter

| Rank | Trainable params | Share of weights | MC1 (mean ± sd) |
|---|---|---|---|
| 1 | 1.2M | 0.07% | 0.417 ± 0.006 |
| 2 | 2.3M | 0.15% | 0.413 ± 0.006 |
| 4 | 4.6M | 0.30% | 0.423 ± 0.015 |
| 8 | 9.2M | 0.60% | 0.450 ± 0.036 |
| 16 | 18.5M | 1.2% | 0.443 ± 0.032 |
| 32 | 36.9M | 2.4% | 0.433 ± 0.025 |
| 64 | 73.9M | 4.8% | 0.447 ± 0.006 |
| 128 | 147.7M | 9.6% | 0.437 ± 0.021 |
| 256 | 295.4M | 19.1% | 0.430 ± 0.035 |

Trainable parameters grow 256× and accuracy stays within the seed-to-seed spread. The models also
get the same questions right: r=8 and r=64 agree question by question about as often as two seeds
of the same rank. Changing the rank changes the answers no more than retraining with a different
random seed. The fixed-α control is flat too, so the α/r scaling is not hiding a rank effect.

The likely reason is the data, not the adapter. The training set is 645 short answers, and even
rank 1 has more trainable parameters than there are training tokens. Best validation loss is flat
across ranks as well. This agrees with Hu et al. (2022), who found low ranks often match high ones,
and with Aghajanyan et al. (2021) on the low intrinsic dimension of fine-tuning. Rank may matter with
much more data or a task that needs new knowledge; this experiment does not test that.

## What fine-tuning actually changed

- **How the model answers, more than what it knows.** The fine-tuned model commits to short answers
  and says "I have no comment" where the benchmark expects it.
- **It is not just picking the shortest option.** MC1 sums log-probabilities, which favors short
  options, and TruthfulQA's true answer is often the shortest. But the fine-tuned model's chosen
  answers are no shorter, accuracy rises whether or not the true answer is the shortest, and
  length-normalized MC1 rises nearly as much (0.37 to 0.51 at r=8).
- **More decisive is not the same as more truthful.** On free-form answers graded by AllenAI's
  TruthfulQA judges, the base model hedges: its answers average about 59 tokens and often open with
  "As an AI", which the judge counts as truthful but uninformative. The fine-tuned model answers in
  about 11 tokens and commits, and some of those commitments are wrong. Informativeness rose and
  truthfulness fell slightly.
- **Confidence does not predict which mistakes get fixed.** I expected fine-tuning to fix uncertain
  mistakes and leave confident misconceptions alone. Splitting the base model's wrong answers by
  confidence showed no such pattern.

## What each option costs

| | LoRA r=8 | LoRA r=64 | Full fine-tune |
|---|---|---|---|
| MC1 | 0.450 | 0.447 | 0.473 |
| Peak GPU memory | 3.8 GB | 4.7 GB | 24.9 GB |
| Training time | 34 s | 27 s | 58 s |
| Saved artifact | 37 MB | 295 MB | 6.2 GB |
| Query latency, unmerged | 41.3 ms | 41.4 ms | n/a |
| Query latency, merged | 20.3 ms | 20.4 ms | 18.6 ms |

Full fine-tuning buys nothing measurable over LoRA here, at 6.6× the memory and a model file 167×
larger than the r=8 adapter.

An unmerged adapter doubles query latency (the base model takes 20.2 ms). That cost is not the
adapter's arithmetic: r=64 costs no more time than r=8, though its arithmetic is 8× larger. It comes
from running separate small operations beside every layer. Merging folds the adapter into the
weights and brings latency back to the base model's. Measured parameter counts match the formula
r·(d<sub>in</sub> + d<sub>out</sub>) over 7 projections in 28 layers exactly at every rank.

## Robustness checks

- **No measurable forgetting.** On MMLU and HellaSwag (lm-evaluation-harness, 0-shot), every change
  after fine-tuning is smaller than the roughly ±4 point noise at 500 items. Training was short,
  which leaves little room to overwrite general skills.
- **No test leakage.** TruthfulQA has reworded variants of some questions. Embedding every question
  with MiniLM flags 6 test questions whose nearest training question is a near-paraphrase. The gain
  on the other 94 is about the same as overall.
- **Same result on a second model family.** SmolLM2-1.7B, trained on different data, starts at
  nearly the same accuracy (0.30) and gains about as much (0.45 at r=8, 0.48 at r=64, inside the
  noise).

## The bug that produced a convincing wrong answer

The first full run showed accuracy rising with rank. It was an artifact.

PyTorch's fused attention kernel returned a NaN gradient on some padded batches while the loss
stayed finite. Early stopping saw validation loss stop improving and restored the last clean
checkpoint, so every run looked normal, just shorter. Run 1 suggested that higher rank helps. After
switching to standard attention and adding a guard that stops on any non-finite value, every
configuration improved and the trend disappeared. Every number on this page is from the corrected
rerun. The lesson I took: read the raw training logs, not only the summary a run writes at the end.

## Limitations

- 100 test questions leave wide intervals: about ±10 points on one model's accuracy, tighter for
  paired comparisons.
- One benchmark and 645 training examples. With more data, or a task that needs new knowledge, rank
  may matter.
- One train/test split, stratified by category; seeds vary training only.
- Free-form judgments come from 7B judge models, so treat them as a second opinion.

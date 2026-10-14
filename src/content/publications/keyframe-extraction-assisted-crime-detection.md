---
title: Keyframe Extraction assisted Crime Detection
subtitle: Ameya G. Jangam, Atharva P. Mohite, Deep U. Nayak, Anant V. Nimkar
meta: IEEE, 2023
order: 2
summary: >-
  How much of a surveillance video can you discard before a model stops recognizing what happened
  in it? Twelve model-and-extractor configurations on UCF-Crime. Best reported average accuracy was 84.53%
  for SlowFast with histogram extraction, and frame selection cut reported per-epoch time by as
  much as 68.75%.
external:
  - { label: "Paper (PDF)", href: "/papers/keyframe-extraction-assisted-crime-detection.pdf" }
---

<div class="glance">
<p class="glance-label">At a glance</p>
<dl>
<dt>Question</dt>
<dd>If an action-recognition model sees only about 10% of a surveillance video's frames, does it get worse at naming the crime, and how much training time does that save?</dd>
<dt>Approach</dt>
<dd>Three recognition models (SlowFast, UniFormerV2, TIN) crossed with three keyframe extractors (VSUMM, SIFT, color histogram), each model also trained on all frames as a baseline. Twelve configurations in total.</dd>
<dt>Data</dt>
<dd>UCF-Crime: Explosion, Assault, Shooting, Fighting, Road Accident, plus Normal.</dd>
<dt>Headline</dt>
<dd>SlowFast with histogram extraction had the best reported average accuracy, 84.53% against 79.20% on all frames. Frame selection cut per-epoch time by up to 68.75%.</dd>
<dt>Takeaway</dt>
<dd>Dropping 90% of the frames usually helped accuracy. The best extractor depends on the kind of crime, and the time saved depends heavily on the architecture.</dd>
</dl>
</div>

## Why this question

Most of a CCTV recording is nothing happening. The conclusion of the paper puts it at roughly 80%
normal activity, with the action that matters somewhere in the remaining 20%. Standard
action-recognition models still read every frame, which makes training and inference slow on long
footage.

Keyframe extraction is the obvious fix: pick a small subset of frames that carry the content and
hand only those to the model. The open question was whether that subset keeps enough of the action
for the model to classify it correctly. Plenty of extractors exist, but we had not found a study
that measured how each one affects action-recognition accuracy on crime footage. So we built the
grid.

The paper names two contributions:

1. A benchmark of state-of-the-art action-recognition models on top of keyframe extraction, on
   UCF-Crime.
2. A parameter-efficient fine-tuning approach claimed to need 90% less training data for a 1 to 2
   point gain. (The body of the paper does not give this its own experiment; see the limitations.)

## The pipeline

<ol class="flow">
<li><b>Read a video</b> from UCF-Crime.</li>
<li><b>Extract keyframes</b> with one chosen algorithm, keeping about 10% of frames.</li>
<li><b>Classify</b> the keyframes with one chosen action-recognition model.</li>
<li><b>Score</b>: the model outputs a confidence per action class.</li>
<li><b>Report</b> the five highest-confidence classes.</li>
</ol>

The extractor and the model are independent slots, so any extractor can be paired with any model.
That modularity is what made a full 3×3 grid, plus baselines, cheap to run.

## What we compared

### Recognition models

The three were picked because their architectures differ in how they handle time, and that is
exactly what removing frames disturbs.

| Model | How it handles time | Why it is in the study |
|---|---|---|
| **SlowFast** | Two pathways: a slow one for spatial semantics and long-range context, a fast one for motion | Built for efficiency; handles short and long temporal structure |
| **UniFormerV2** | Pretrained image ViTs plus UniFormer blocks that combine convolution (local) and self-attention (global) | Attention compares every frame with every other, so it pays most per frame |
| **TIN** | Temporal Interlacing Network; one stream at one temporal resolution, interlaces features across time | Targets fast-changing actions; the simplest of the three |

### Keyframe extractors

| Extractor | Picks frames by | Strength | Weakness |
|---|---|---|---|
| **VSUMM** | Clustering similar frames and choosing a representative from each cluster | Broad, representative coverage of the whole video | Sensitive to clustering and heuristic choices |
| **SIFT** | Distinctive local features that survive changes in scale, rotation, and translation | Holds onto specific people and objects | Can skip frames that lack distinctive features |
| **Histogram** | Large shifts in color or texture distribution between frames | Simple and adaptable | Ignores changes that do not show up in color |

## Setup

- **Data.** UCF-Crime has 128 hours of untrimmed real-world surveillance video: 1,900 videos over
  13 anomaly types (Abuse, Arrest, Arson, Assault, Road Accident, Burglary, Explosion, Fighting,
  Robbery, Shooting, Stealing, Shoplifting, Vandalism). To keep training manageable we used five
  of them plus Normal.
- **Hardware.** One Tesla K80 with 12 GB, for both training and evaluation.
- **Budget.** 25 epochs per configuration.
- **Frame budget.** After experimenting, we found about 10% of a video's frames captured most of
  the important content.
- **Model specifics.** SlowFast had the largest memory footprint (about 150 MB loaded), which
  limited it to batch size 10. UniFormerV2 trained with batch size 20 at a learning rate of 5e-5,
  and its per-frame attention made it the slowest to train. Batch sizes were adjusted per model to
  fit in GPU memory.

## Result 1: training time

Reported time per epoch, with and without keyframe extraction.

<div class="chart">
<p class="chart-title">Reduction in time per epoch with keyframe extraction</p>
<div class="bar"><span class="bar-label">UniFormerV2 + VSUMM</span><span class="bar-track"><span class="bar-fill" style="--w:68.75%"></span></span><span class="bar-value">68.75%</span></div>
<div class="bar"><span class="bar-label">SlowFast + VSUMM</span><span class="bar-track"><span class="bar-fill" style="--w:67.12%"></span></span><span class="bar-value">67.12%</span></div>
<div class="bar"><span class="bar-label">UniFormerV2 + SIFT</span><span class="bar-track"><span class="bar-fill" style="--w:66.15%"></span></span><span class="bar-value">66.15%</span></div>
<div class="bar"><span class="bar-label">SlowFast + histogram</span><span class="bar-track"><span class="bar-fill" style="--w:65.28%"></span></span><span class="bar-value">65.28%</span></div>
<div class="bar"><span class="bar-label">UniFormerV2 + histogram</span><span class="bar-track"><span class="bar-fill" style="--w:63.54%"></span></span><span class="bar-value">63.54%</span></div>
<div class="bar"><span class="bar-label">SlowFast + SIFT</span><span class="bar-track"><span class="bar-fill" style="--w:54.86%"></span></span><span class="bar-value">54.86%</span></div>
<div class="bar"><span class="bar-label">TIN + SIFT</span><span class="bar-track"><span class="bar-fill" style="--w:17.46%"></span></span><span class="bar-value">17.46%</span></div>
<div class="bar"><span class="bar-label">TIN + VSUMM</span><span class="bar-track"><span class="bar-fill" style="--w:7.94%"></span></span><span class="bar-value">7.94%</span></div>
<div class="bar"><span class="bar-label">TIN + histogram</span><span class="bar-track"><span class="bar-fill" style="--w:4.76%"></span></span><span class="bar-value">4.76%</span></div>
<p class="chart-note">Scale 0 to 100%. From Table I of the paper.</p>
</div>

| Model | Extractor | Hours/epoch with | Hours/epoch without | Reduction |
|---|---|---|---|---|
| SlowFast | Histogram | ~1.0 | ~2.88 | 65.28% |
| SlowFast | VSUMM | ~0.9 | ~2.88 | 67.12% |
| SlowFast | SIFT | ~1.3 | ~2.88 | 54.86% |
| UniFormerV2 | Histogram | ~1.4 | ~3.84 | 63.54% |
| UniFormerV2 | VSUMM | ~1.2 | ~3.84 | 68.75% |
| UniFormerV2 | SIFT | ~1.3 | ~3.84 | 66.15% |
| TIN | Histogram | ~3.0 | ~3.15 | 4.76% |
| TIN | VSUMM | ~2.9 | ~3.15 | 7.94% |
| TIN | SIFT | ~2.6 | ~3.15 | 17.46% |

The split is about architecture, not about the extractor. SlowFast and UniFormerV2 save roughly
two-thirds of their epoch time. TIN saves 5 to 17%. The paper's explanation is that UniFormerV2's
self-attention compares every frame with every other frame, so its cost falls quickly as frames
are removed, while SlowFast relies on motion and texture change, which the extractors keep. TIN
works at a single temporal resolution, and its cost barely moves.

## Result 2: average accuracy

Each model compared with its own all-frames baseline.

| Model | All frames | Histogram | VSUMM | SIFT |
|---|---|---|---|---|
| SlowFast | 79.20 | **84.53** (+5.33) | 83.05 (+3.85) | 82.10 (+2.90) |
| UniFormerV2 | 79.46 | 80.14 (+0.68) | 81.73 (+2.27) | 79.09 (−0.37) |
| TIN | 78.76 | 82.21 (+3.45) | 80.92 (+2.16) | 83.60 (+4.84) |

<div class="chart">
<p class="chart-title">Change in average accuracy versus all frames (points)</p>
<div class="bar"><span class="bar-label">SlowFast + histogram</span><span class="bar-track"><span class="bar-fill" style="--w:100%"></span></span><span class="bar-value">+5.33</span></div>
<div class="bar"><span class="bar-label">TIN + SIFT</span><span class="bar-track"><span class="bar-fill" style="--w:90.8%"></span></span><span class="bar-value">+4.84</span></div>
<div class="bar"><span class="bar-label">SlowFast + VSUMM</span><span class="bar-track"><span class="bar-fill" style="--w:72.2%"></span></span><span class="bar-value">+3.85</span></div>
<div class="bar"><span class="bar-label">TIN + histogram</span><span class="bar-track"><span class="bar-fill" style="--w:64.7%"></span></span><span class="bar-value">+3.45</span></div>
<div class="bar"><span class="bar-label">SlowFast + SIFT</span><span class="bar-track"><span class="bar-fill" style="--w:54.4%"></span></span><span class="bar-value">+2.90</span></div>
<div class="bar"><span class="bar-label">UniFormerV2 + VSUMM</span><span class="bar-track"><span class="bar-fill" style="--w:42.6%"></span></span><span class="bar-value">+2.27</span></div>
<div class="bar"><span class="bar-label">TIN + VSUMM</span><span class="bar-track"><span class="bar-fill" style="--w:40.5%"></span></span><span class="bar-value">+2.16</span></div>
<div class="bar"><span class="bar-label">UniFormerV2 + histogram</span><span class="bar-track"><span class="bar-fill" style="--w:12.8%"></span></span><span class="bar-value">+0.68</span></div>
<div class="bar dim"><span class="bar-label">UniFormerV2 + SIFT</span><span class="bar-track"><span class="bar-fill" style="--w:6.9%"></span></span><span class="bar-value">−0.37</span></div>
<p class="chart-note">Gray bar is the one decline. Bar length is proportional to the size of the change.</p>
</div>

Eight of the nine pairings beat their baseline. The only decline was UniFormerV2 with SIFT, down
0.37 points. That is the counterintuitive part: removing 90% of the frames almost always helped. A
plausible reading is that the extractors also act as a denoiser, removing long stretches of
irrelevant footage that otherwise dilute the signal, though the paper did not test that directly.

<figure>
<img src="/papers/figures/keyframe-accuracy-vs-epochs.jpg" alt="Line chart of average accuracy against epochs 0 to 25 for all twelve configurations, rising from about 60-70% to about 79-85%." width="1042" height="557" loading="lazy" />
<figcaption>Fig. 2 from the paper: average accuracy over 25 epochs for every configuration. Most curves are still rising at epoch 25, so the budget, not convergence, set the final numbers. (Some legend colors repeat in the original.)</figcaption>
</figure>

<div class="note">

**A caution on the averages.** The "average accuracy" column does not match the mean of the paper's
own six per-class tables. For SlowFast with histogram, the unweighted mean of the six class
accuracies is 82.14, not 84.53. Taking the unweighted mean of every row, TIN with histogram comes
out highest (83.39) and UniFormerV2 with SIFT becomes a gain rather than a decline. The paper does
not say how the average was computed. It may be weighted by the number of test clips per class,
but per-class counts are not reported, so I cannot confirm that. I treat the ranking among the top
configurations as unsettled, and the broader finding (extraction helps nearly everywhere) as
robust, because it holds under both readings.

</div>

## Result 3: the best extractor depends on the crime

Per-class accuracy (%) for every configuration. The best result in each column is highlighted.

| Configuration | Explosion | Shooting | Fighting | Assault | Road Accident | Normal |
|---|---|---|---|---|---|---|
| SlowFast, all frames | 78.95 | 79.22 | 77.89 | 78.12 | 77.23 | 77.47 |
| SlowFast + histogram | 81.65 | 80.25 | 82.92 | 81.39 | 84.31 | 82.31 |
| SlowFast + VSUMM | <span class="best">85.43</span> | <span class="best">85.21</span> | 81.36 | 80.51 | 80.72 | 79.89 |
| SlowFast + SIFT | 80.32 | 80.27 | 83.72 | 83.36 | 81.89 | 83.58 |
| UniFormerV2, all frames | 79.54 | 81.90 | 76.98 | 77.59 | 76.61 | 77.60 |
| UniFormerV2 + histogram | 82.47 | 79.92 | 79.13 | 80.47 | 80.43 | 83.81 |
| UniFormerV2 + VSUMM | 84.62 | 84.71 | 80.74 | 81.14 | 81.62 | 80.12 |
| UniFormerV2 + SIFT | 79.57 | 80.32 | 81.53 | <span class="best">84.83</span> | 82.98 | 82.77 |
| TIN, all frames | 80.19 | 79.42 | 77.25 | 79.73 | 77.01 | 77.34 |
| TIN + histogram | 82.57 | 81.34 | 83.94 | 83.14 | <span class="best">85.07</span> | <span class="best">84.25</span> |
| TIN + VSUMM | 83.90 | 84.63 | 81.81 | 82.57 | 82.08 | 81.21 |
| TIN + SIFT | 80.26 | 78.96 | <span class="best">84.00</span> | 84.69 | 83.45 | 83.14 |

The winners line up by extractor in a way that is easy to explain:

- **VSUMM wins Explosion and Shooting.** These are events with distinct phases: the blast, the
  aftermath, people reacting, the emergency response. A clustering method that samples each phase
  covers them well.
- **SIFT wins Fighting and Assault**, and gives each of the three models its best Assault score. The signal is
  in particular people, clothing, and weapons, which is what distinctive local features follow.
- **Histogram wins Road Accident and Normal.** A crash changes the scene's color and texture
  distribution: damaged vehicles, stopped traffic, debris.

These explanations come after the fact. We did not run the feature-level analysis or significance
tests that would establish them as causes, and some margins are under a point.

## Conclusion

Keyframe extraction is worth doing before action recognition on long surveillance video. It
reduces training time by about two-thirds on SlowFast and UniFormerV2 and raises accuracy on
almost every pairing. The paper concludes that SlowFast with histogram extraction is the best
overall combination. It is not the fastest configuration, and given the averaging caution above,
"strong overall choice" is the claim I would defend. The more useful result for a practitioner is
the per-class one: if you know what kind of event you are looking for, choose the extractor to
match it.

## Limitations

These are worth stating plainly. The paper records what an undergraduate team could run and check
on one K80.

- **Evaluation protocol is not documented.** No train/test split, per-class video counts, or
  description of how the average was aggregated (see the caution above).
- **Inconsistent time terminology.** The paper uses "training time", "time per epoch", and
  "inference time" interchangeably. Table I measures hours per epoch, so that is the claim. The
  setup text also gives per-epoch times (1 to 1.5 h for SlowFast, 1.5 to 1.75 h for UniFormerV2)
  that do not line up with either column of Table I.
- **No repeated runs, confidence intervals, or significance tests.** Many per-class gaps between
  configurations are under one point.
- **The parameter-efficient fine-tuning claim has no experiment behind it.** The introduction
  promises 90% less data for a 1 to 2 point gain, and a section on it is announced, but the body
  has no separate method description, ablation, or results table for it.
- **Scope.** Five crime classes plus Normal, not the full 13-class dataset. The 25-epoch cap
  stopped training while accuracy was still rising.
- **No confusion matrix or error analysis.** The per-class explanations are never checked against
  the frames that were actually selected.
- **The real-time web application mentioned in the introduction is not described.**

## What I would do differently

- Report class-weighted and unweighted averages and the split, so readers can check the ranking.
- Run at least three seeds per configuration and report variance before calling a winner.
- Vary the frame budget (5%, 10%, 25%, 50%) instead of fixing it at 10%, to locate where accuracy
  begins to fall.
- Separate training cost from inference latency and measure each directly.
- Look at which frames each extractor keeps for a sample of videos, to test the per-class
  explanations instead of assuming them.

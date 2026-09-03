---
title: Keyframe Extraction assisted Crime Detection
subtitle: Ameya G. Jangam, Atharva P. Mohite, Deep U. Nayak, Anant V. Nimkar
meta: IEEE, 2023
order: 2
summary: >-
  How much of a surveillance video can you discard before a model stops recognizing what happened
  in it? Twelve model-and-extractor configurations on UCF-Crime. Best average accuracy was 84.53%
  for SlowFast with histogram extraction, and frame selection cut reported per-epoch time by as
  much as 68.75%.
external:
  - { label: "Paper (PDF)", href: "/papers/keyframe-extraction-assisted-crime-detection.pdf" }
---

## The question

Long surveillance video is mostly redundant. Process every frame and you pay for it in training
and inference cost. Drop too many, or the wrong ones, and you delete the evidence the model needed
to classify the action at all.

So we ran the full grid: three action-recognition models against three keyframe-extraction
algorithms, plus each model with no extraction as its own baseline. Twelve configurations.

## What we compared

**Recognition models**

- **SlowFast**, two pathways, one for slow semantic structure and one for fast motion.
- **UniFormerV2**, convolution plus attention, learning short-range and long-range relationships.
- **TIN**, Temporal Interlacing Network, interlacing temporal information for fast-changing actions.

**Frame selection**

- **VSUMM**, clusters similar frames and picks representatives.
- **SIFT**, scale and rotation invariant local features, favoring frames with distinctive structure.
- **Histogram comparison**, selects frames around shifts in color or texture distribution.

## Setup

UCF-Crime is 128 hours of 1,900 untrimmed real-world surveillance videos across 13 anomaly types.
For tractable experimentation we focused on five: Explosion, Assault, Shooting, Fighting, and Road
Accident, with a Normal class alongside them.

Training ran on a single Tesla K80 with 12 GB, capped at 25 epochs per pairing. Experimentation
suggested roughly 10% of a video's frames retain a substantial portion of its important content.

## Results: accuracy

Average accuracy across the included classes, and the change against each model's own no-keyframe
baseline.

| Model | Baseline | Histogram | VSUMM | SIFT |
|---|---|---|---|---|
| SlowFast | 79.20 | **84.53** (+5.33) | 83.05 (+3.85) | 82.10 (+2.90) |
| UniFormerV2 | 79.46 | 80.14 (+0.68) | 81.73 (+2.27) | 79.09 (-0.37) |
| TIN | 78.76 | 82.21 (+3.45) | 80.92 (+2.16) | 83.60 (+4.84) |

Every configuration but one beat its baseline. The single decline was UniFormerV2 with SIFT, 0.37
points down. That is the useful finding buried in the grid: throwing away 90% of the frames almost
always *helped*, which is not the intuition you start with.

## Results: time

Reported per-epoch time, with and without extraction.

| Pairing | Reduction |
|---|---|
| UniFormerV2 + VSUMM | 68.75% |
| SlowFast + VSUMM | 67.12% |
| UniFormerV2 + SIFT | 66.15% |
| SlowFast + histogram | 65.28% |
| TIN + SIFT | 17.46% |
| TIN + histogram | 4.76% |

TIN barely benefits. SlowFast and UniFormerV2 benefit enormously. The cost of a frame is not the
same across architectures, and that shows up here more clearly than in any accuracy number.

## Which extractor wins depends on the crime

Per-class, the winners split along an interpretable line:

- **VSUMM** takes Explosion (85.43) and Shooting (85.21), events where broad scene coverage matters.
- **SIFT** takes Fighting (84.00) and Assault (84.83), where distinctive people, clothing, or
  objects carry the signal.
- **Histogram** takes Road Accident (85.07), where damaged vehicles and changed traffic shift the
  color and texture distribution.

These are plausible post-hoc readings. We did not run the feature-level analysis or significance
testing that would be needed to establish them causally.

## Conclusion

SlowFast with histogram extraction gives the best balance at 84.53% average accuracy. It is not
the fastest configuration, so "best balance" is the honest phrasing, not "fastest."

## Limitations

Worth stating plainly, since the paper is a snapshot of what an undergraduate team could verify:

- Dataset splits, per-class video counts, and the evaluation protocol are not documented.
- The paper uses "training time", "time per epoch", and "inference time" inconsistently. The table
  measures per-epoch time in hours, so that is the claim I stand behind.
- No repeated runs, confidence intervals, or significance tests.
- The parameter-efficient fine-tuning contribution claimed in the introduction is not backed by a
  separate results table in the body.
- No confusion matrix or error analysis.

These numbers describe the reported experiment on five UCF-Crime classes plus Normal. They are not
a result on the full 13-class dataset.

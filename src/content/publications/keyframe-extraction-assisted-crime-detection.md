---
title: Keyframe Extraction assisted Crime Detection
subtitle: Ameya G. Jangam, Atharva P. Mohite, Deep U. Nayak, Anant V. Nimkar
meta: IEEE, 2023
order: 2
summary: >-
  How much of a surveillance video can you throw away before a model stops recognizing what
  happened in it? Best configuration reached 84.53% average accuracy, 5.33 points over baseline,
  while cutting per-epoch processing time by up to 68.75%.
---

## The question

Long surveillance video is mostly redundant. Process every frame and you pay for it in training and
inference cost. Drop too many, or the wrong ones, and you delete the evidence the model needed.

We evaluated 12 combinations: three action-recognition models against three keyframe-extraction
algorithms, on selected UCF-Crime classes.

## The models

- **SlowFast**, two pathways, one for slow semantic structure and one for fast motion.
- **UniFormerV2**, convolution plus attention, for short-range and long-range video relationships.
- **TIN**, Temporal Interlacing Network, interlacing temporal information for fast-changing actions.

## The extractors

Histogram comparison, VSUMM, and SIFT.

## Results

TODO: fill in the full grid. Which pairing won and why, and whether the speed-accuracy tradeoff
behaved the way you expected.

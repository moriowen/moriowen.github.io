---
title: Leveraging LLMs for Video Querying
subtitle: Ameya G. Jangam, Atharva P. Mohite, Deep U. Nayak, Anant V. Nimkar
meta: IEEE, 2023
order: 1
summary: >-
  Ask a long surveillance video a question in plain English and get back the timestamps where it
  happened. Dense captioning with BMT or Vid2Seq, then an LLM over the timestamped captions. GPT-4
  reached 56% exact timestamp matching and 85% within a two-minute tolerance.
external:
  - { label: "Paper (PDF)", href: "/papers/leveraging-llms-for-video-querying.pdf" }
  - { label: "Project report (PDF)", href: "/papers/leveraging-llms-for-video-querying-project-report.pdf" }
---

## The problem

Finding a moment in a long video means either watching all of it or trusting metadata too coarse to
help. Neither gives precise event localization.

The idea: convert the video into timestamped text, hand an LLM both that text and a natural-language
query, and have it return the interval where the event occurred. Language becomes the retrieval
layer over video.

## Research questions

1. Can LLMs combine with video-captioning transformers to do a multimodal task without retraining
   the LLM on the domain?
2. What does a chain of modal conversions cost, going video and audio to captions to an answer?
3. Why do different LLMs perform so differently on long crime videos?
4. How much do captioning-model choice, domain fine-tuning, and prompt specificity matter?

## The pipeline

1. A captioning model divides the video into temporal regions.
2. It generates a caption per region, preserving start and end times.
3. An accumulator assembles a timestamped textual representation of the whole video.
4. The user submits a natural-language query.
5. The LLM reads the captions plus the query.
6. It returns one or more predicted intervals, as start time, end time, and the sentence that
   describes them.

**BMT path.** I3D visual features and VGGish audio features fused by a bi-modal encoder, a proposal
generator that selects temporal regions and attaches timestamps, and a bi-modal decoder fine-tuned
for crime captions. The proposal generator matters more than it sounds: it keeps captioning aligned
to the visual evidence in time.

**Vid2Seq path.** Visual embeddings and a Google Cloud audio transcription processed by separate
encoders, concatenated, then decoded to captions.

## The context window problem

A long surveillance video produces more caption text than the LLM can read at once. The recursive
strategy splits the captions into chunks, appends the query to each, processes them independently,
keeps the intermediate answers, and repeats over the survivors, halving the set each pass until
what remains fits in one context window.

This was the constraint that shaped the architecture, and it is the part that dates the paper most:
we were working against 2023 context limits.

## Annotation

We hand-annotated 50 UCF-Crime videos through a multi-annotator consensus process. Three annotators
independently described randomly selected frames in one sentence each; where they diverged
substantially, a fourth broke the tie. Instructions emphasized brief, relevant descriptions of
visible objects, actions, and context.

The aim was to reduce individual annotator bias while producing domain-specific frame-caption
pairs. The dataset was not released or independently validated.

## Metric

For each ground-truth segment we compare predicted against expected boundaries at three tolerances:

- **Exact**: both boundaries match.
- **One-minute deviation**: absolute start and end errors sum to at most 2 minutes.
- **Two-minute deviation**: they sum to at most 4 minutes.

This is boundary-error tolerance, not temporal intersection over union.

## Results

Percentage of segments accepted at each tolerance.

| Model | Exact | Within 1 min | Within 2 min |
|---|---|---|---|
| **GPT-4** | **56** | **77** | **85** |
| GPT-3.5 | 53 | 72 | 80 |
| LLaMA | 52 | 73 | 78 |

GPT-4 leads at every tolerance, by 3 to 5 points over GPT-3.5 and 4 to 7 over LLaMA. The gap
between exact matching and two-minute tolerance is the more interesting number: the pipeline is
much better at finding roughly where something happened than exactly when.

## Conclusion

Video search decomposes cleanly into dense captioning plus language-based retrieval, and an LLM
given enough timestamped text can answer event queries over video it was never trained on.

Two honest caveats on the conclusions. Only the timestamp table above is quantified. Our findings
that BMT suited long-form crime video better than Vid2Seq, that domain fine-tuning improved the
captioning models, and that the architecture is commercially feasible are project conclusions, not
independently measured results.

## Limitations

- No caption-quality metric directly comparing BMT and Vid2Seq.
- No baseline against embedding search, keyword search, or a direct temporal-grounding model.
- Prompt templates, model versions, and generation parameters are not recorded.
- Evaluation sample size is not stated, and segment matching across multiple occurrences is
  underspecified.
- The one and two-minute tolerances are generous for short events.
- The paper reports 100 epochs at ~1.5 hours each alongside a 30-hour total, which cannot both be
  true. The project report says 20 epochs, which is consistent with 30 hours.

## What I would change

TODO: this predates long-context models and native video understanding. Worth writing down what
holds up, what the recursive chunking would be replaced by now, and whether the captioning
bottleneck is still the bottleneck.

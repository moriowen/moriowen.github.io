---
title: Leveraging LLMs for Video Querying
subtitle: Ameya G. Jangam, Atharva P. Mohite, Deep U. Nayak, Anant V. Nimkar
meta: IEEE, 2023
order: 1
summary: >-
  Turns long video into timestamped captions with BMT and Vid2Seq, then lets an LLM answer
  natural-language questions about it. GPT-4 reached 56% exact timestamp matching and 85% within a
  two-minute tolerance on UCF-Crime.
---

## The problem

Searching a long video means either watching it or trusting coarse metadata. Neither gives you
precise event localization. We convert the video into timestamped textual captions, hand an LLM
both the captions and a natural-language query, and ask it to return the interval where the event
happened.

## Research questions

1. Can LLMs combine with video-captioning transformers to do a multimodal task without retraining
   the LLM on the domain?
2. What does the chain of modal conversions cost, going video and audio, to captions, to an LLM
   response?
3. Why do different LLMs perform so differently on long crime videos?
4. How much do captioning-model choice, domain fine-tuning, and prompt specificity matter?

## Results

TODO: expand. The comparison across GPT-3.5, GPT-4, and LLaMA, the context-window ceiling on long
videos, and where the pipeline loses information.

## What I would change

TODO: this predates modern long-context and native video models. Worth saying what holds up and
what does not.

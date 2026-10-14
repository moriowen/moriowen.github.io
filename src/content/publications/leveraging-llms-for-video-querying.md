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

<div class="glance">
<p class="glance-label">At a glance</p>
<dl>
<dt>Question</dt>
<dd>Can an off-the-shelf LLM find when something happens in a long video, if the video is first turned into timestamped text?</dd>
<dt>Approach</dt>
<dd>A dense video captioner (BMT or Vid2Seq), fine-tuned on crime footage, writes a caption for each time region. An LLM reads the captions plus a natural-language query and returns the matching start and end times.</dd>
<dt>Data</dt>
<dd>50 UCF-Crime videos we hand-annotated through multi-annotator consensus.</dd>
<dt>Headline</dt>
<dd>GPT-4 returned the exact segment 56% of the time, 77% within a one-minute tolerance, and 85% within two minutes. GPT-3.5 and LLaMA trailed by 3 to 7 points.</dd>
<dt>Takeaway</dt>
<dd>Language works as a retrieval layer over video. The pipeline finds roughly where an event happened far more reliably than exactly when.</dd>
</dl>
</div>

This was my B.Tech final-year project (May 2023, guided by Dr. Anant V. Nimkar) and the six-page
IEEE paper that came out of it. The project report linked above is the long version: 38 pages
with fuller architecture diagrams and the training details.

## The problem

Finding a moment in a long video means either watching all of it or relying on metadata tags and
manual annotations that are too coarse to help. For surveillance footage that is hours of
watching, and a mistake has real consequences.

The idea: turn the video into timestamped text, give an LLM that text and a plain-English
question, and have it return the interval where the event happens. The LLM never sees a pixel. It
reasons over a written log of the video.

## Research questions

1. Can LLMs be combined with video-captioning transformers to handle a multimodal task without
   adapting the LLM to the domain?
2. What does a chain of modality conversions cost (video and audio to captions, captions to an
   answer) when captioning crime footage?
3. Why do different LLMs perform so differently when querying long crime videos?

The project report adds objectives about prompt design (how specific a query should be) and
about the effect of domain fine-tuning on the captioners.

## The pipeline

<ol class="flow">
<li><b>Propose regions.</b> The captioning model splits the video into temporal regions where something is happening.</li>
<li><b>Caption each region</b> in one sentence, keeping its start and end time.</li>
<li><b>Accumulate</b> those into a timestamped transcript of the whole video: a list of <code>{start, end, sentence}</code>.</li>
<li><b>Query.</b> The user writes a question, e.g. "Identify the exact moment when a car accident occurs in the video."</li>
<li><b>Reduce.</b> If the transcript is too long for the LLM's context window, the recursive strategy (below) shrinks it.</li>
<li><b>Answer.</b> The LLM returns one or more intervals, each with a start time, end time, and the caption that matched.</li>
</ol>

Two captioners fill step 1 and 2. Everything after the caption accumulator is shared.

### Path A: Bi-Modal Transformer (BMT)

<figure>
<img src="/papers/figures/llm-bmt-architecture.png" alt="Architecture diagram: video footage produces VGGish audio and I3D image embeddings, which feed a stack of bi-modal encoders, a proposal generator, and bi-modal decoders; the captions go to a caption accumulator, a recursive LLM strategy, and an LLM that receives the user's query and returns the timestamp and caption of the event." width="708" height="651" loading="lazy" />
<figcaption>Fig. 1 from the paper: the BMT path from footage to returned timestamp.</figcaption>
</figure>

- **I3D** features encode what is visible; **VGGish** features encode the audio.
- A stack of **bi-modal encoders** fuses the two with self-attention, so sound can inform what is
  seen and the reverse.
- A **proposal generator** chooses which temporal regions are worth captioning and attaches their
  timestamps. This is the piece that keeps captions aligned with the visual evidence in time.
- **Bi-modal decoders**, fine-tuned on our crime captions, write one sentence per region.

### Path B: Vid2Seq

<figure>
<img src="/papers/figures/llm-vid2seq-architecture.png" alt="Architecture diagram: video frames go through a spatial encoder and temporal encoders, transcribed text goes through a token embedder and text encoders; both feed text decoders, whose captions go to the same caption accumulator, recursive LLM strategy, and LLM." width="681" height="651" loading="lazy" />
<figcaption>Fig. 2 from the paper: the Vid2Seq path. Only the captioner changes.</figcaption>
</figure>

- Audio is first transcribed to text with the **Google Cloud** speech API.
- Video frames go through a spatial encoder and then temporal encoders. The transcript goes
  through a token embedder and text encoders.
- The two representations are concatenated and decoded into time-localized captions.

The difference that matters: BMT fuses raw audio features with vision, while Vid2Seq first
converts audio to words. On surveillance footage, where audio is often noise rather than speech,
that is a real design choice.

## The context window problem

A long surveillance video produces more caption text than a 2023 LLM could read at once. The
recursive strategy handles that:

<ol class="flow">
<li><b>Split</b> the transcript into chunks that each fit in the context window.</li>
<li><b>Ask each chunk</b> the same query, independently.</li>
<li><b>Keep</b> the intermediate answers in a temporary store.</li>
<li><b>Repeat</b> over the surviving answers, roughly halving the set each pass.</li>
<li><b>Stop</b> once everything left fits in one context window, and answer from that.</li>
</ol>

Because each chunk is queried separately, an event that happens more than once (a crowd forming
twice, for example) can be found in different parts of the video rather than collapsed into one
answer.

This constraint shaped the architecture more than anything else, and it is also what dates the
paper most.

## Writing the query

Query wording turned out to be a trade-off:

- **Specific** queries ("the exact moment a car accident occurs") target one event precisely.
- **Generic** queries ("the timestamp of a crowd gathering") catch more occurrences, at the cost
  of precision.

The recommended prompt balances specificity, context, and generality. When a generic prompt
returns many candidates, the recursive reduction prunes them. We did not quantify this trade-off
separately; it is an observation from building the system.

## Building the caption dataset

No crime-specific caption dataset existed in the form we needed, so we made one from 50 UCF-Crime
videos:

<ol class="flow">
<li><b>Sample</b> frames at random from each video.</li>
<li><b>Annotate independently.</b> Three annotators each describe the frame in one sentence.</li>
<li><b>Resolve disagreement.</b> Where the three diverge substantially, a fourth annotator breaks the tie.</li>
<li><b>Keep it short.</b> Guidelines asked for brief, relevant descriptions of visible objects, actions, and context.</li>
</ol>

The goal was to reduce any single annotator's bias while producing frame-caption pairs in the
vocabulary of crime footage. The resulting pairs were used to fine-tune both captioners and as
reference points for evaluation. The dataset was not released or independently validated.

## Training

| Setting | Value |
|---|---|
| Initialization | Pretrained image-captioning weights |
| Fine-tuning data | Our crime frame-caption pairs |
| Batch size | 32 |
| Optimizer | Adam, learning rate 0.001 |
| Augmentation | Random crop, flip, rotation |
| Hardware | 4× NVIDIA V100 |
| Epoch time | ~1.5 hours |
| Total training | ~30 hours |
| Epochs | 20 (project report); the paper says 100 |

The paper's 100 epochs at 1.5 hours each would take 150 hours, not 30. The project report says 20
epochs, which matches the 30-hour total, and its loss curves for BMT run from epoch 0 to 20. I
take 20 as correct.

## Measuring the answer

For each ground-truth segment (start *l*, end *r*), compare the predicted boundaries and add up the
start and end errors, in minutes:

<div class="glance">
<dl>
<dt>Exact</dt>
<dd>|l − l<sub>pred</sub>| + |r − r<sub>pred</sub>| = 0</dd>
<dt>±1 minute</dt>
<dd>|l − l<sub>pred</sub>| + |r − r<sub>pred</sub>| ≤ 2</dd>
<dt>±2 minutes</dt>
<dd>|l − l<sub>pred</sub>| + |r − r<sub>pred</sub>| ≤ 4</dd>
</dl>
</div>

Worked example: the true event runs 2:00 to 4:00 and the model answers 2:00 to 5:00. The total
error is one minute, so it fails the exact test and passes the one-minute tolerance.

This is a boundary-error tolerance, not temporal intersection-over-union. It is easy to read, but a
two-minute tolerance is generous for an event that only lasts seconds.

## Results

Percentage of ground-truth segments matched at each tolerance.

| Model | Exact | Within 1 min | Within 2 min |
|---|---|---|---|
| **GPT-4** | **56** | **77** | **85** |
| GPT-3.5 | 53 | 72 | 80 |
| LLaMA | 52 | 73 | 78 |

<div class="chart">
<p class="chart-title">GPT-4: segments matched as tolerance loosens</p>
<div class="bar"><span class="bar-label">Exact</span><span class="bar-track"><span class="bar-fill" style="--w:56%"></span></span><span class="bar-value">56%</span></div>
<div class="bar"><span class="bar-label">Within 1 minute</span><span class="bar-track"><span class="bar-fill" style="--w:77%"></span></span><span class="bar-value">77%</span></div>
<div class="bar"><span class="bar-label">Within 2 minutes</span><span class="bar-track"><span class="bar-fill" style="--w:85%"></span></span><span class="bar-value">85%</span></div>
<p class="chart-note">Scale 0 to 100%. GPT-3.5 and LLaMA follow the same shape, 3 to 7 points lower; see the table.</p>
</div>

Two things stand out:

- **GPT-4 leads at every tolerance**, by 3 to 5 points over GPT-3.5 and 4 to 7 over LLaMA. LLaMA
  edges GPT-3.5 at one minute (73 against 72) and falls behind at two.
- **The gap between columns is the more informative number.** Going from exact to two-minute
  tolerance adds 29 points for GPT-4. The pipeline is much better at locating roughly where
  something happened than at pinning its boundaries. My reading is that the boundaries come from
  the captioner's proposal generator, so the LLM can only be as precise as the region edges it is
  given.

The paper attributes GPT-4's lead to model size and broader training. That is reasonable but was
not tested. The paper also describes LLaMA as specialized for video captioning, which is wrong:
LLaMA is a general-purpose language model, and in this pipeline it only ever saw text.

## Conclusions

- Video search breaks down cleanly into dense captioning followed by language-based retrieval. An
  LLM given enough timestamped text can answer event queries about video it was never trained on.
- The paper concludes that BMT produced more relevant captions for long-form crime video than
  Vid2Seq, that fine-tuning on the crime caption set improved both captioners, and that a
  commercial system on this architecture is feasible.

Only the timestamp table is quantified. The last three conclusions are project conclusions from
working with the system, not separately measured results, and I present them that way.

## Limitations

- **No caption-quality metric** (BLEU, METEOR, CIDEr, or similar) comparing BMT with Vid2Seq, or
  before and after fine-tuning.
- **No baselines** against keyword search over captions, embedding similarity search, or a
  dedicated temporal-grounding model.
- **Prompts are not reproducible.** Prompt templates, model versions, dates of API use, sampling
  settings, and the rule for parsing free-text answers into intervals are not recorded.
- **Evaluation details are thin.** The number of query segments is not stated, and how multiple
  occurrences are matched to predictions is underspecified.
- **Possible leakage.** Neither document says whether the videos used to fine-tune the captioners
  were held out from the videos used to evaluate retrieval. A clean version would split by source
  video before sampling frames.
- **Generous tolerances** for short events, as noted above.
- **The epoch discrepancy** between the paper (100) and the report (20).

## What I would change

TODO: this predates long-context models and native video understanding. Worth writing down what
holds up, what the recursive chunking would be replaced by now, and whether the captioning
bottleneck is still the bottleneck.

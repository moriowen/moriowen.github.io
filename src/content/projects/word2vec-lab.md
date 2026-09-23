---
title: Word2Vec Lab
meta: PyTorch, gensim, Python
order: 2
summary: >-
  Five word embedding models trained, downloaded, and fine-tuned on the same corpus, then scored
  through one untuned classifier so every difference is attributable to the embeddings. Includes
  skip-gram with negative sampling written from scratch, and a control run that corrected the
  project's own headline claim.
external:
  - label: Live
    href: https://word2vec-lab.vercel.app/
  - label: Code
    href: https://github.com/moriowen/word2vec-lab
bullets:
  - Trained five models on 633,720 tokens of the Stanford Sentiment Treebank, covering skip-gram and CBOW in gensim, skip-gram with negative sampling written from scratch in PyTorch, GoogleNews-300 frozen, and GoogleNews fine-tuned. All five run through one logistic regression that is never tuned per model.
  - Isolated what a pretrained warm start is worth by adding a control matched on learning rate and epochs. It is +0.127 test accuracy, 0.665 to 0.792, four times what the uncontrolled comparison implied.
  - Found that models with no measurable correlation to human similarity judgements, Spearman 0.029 on WordSim-353, still score 0.761 on sentiment, so downstream accuracy alone would have rated them nearly as good as GoogleNews.
---

## What it is

Word2Vec is two matrices and a dot product, which makes it small enough to implement and still
large enough to ask real questions of. I trained five variants on the same 633,720 tokens of movie
reviews and scored all of them the same way: look up a vector per word, average into a sentence
vector, fit logistic regression, test on the same 1,821 held-out sentences. The classifier never
changes and is never tuned per model, so any gap between the numbers belongs to the embeddings.

## The control that changed the answer

The obvious comparison is the model I trained from scratch against the one warm-started from
Google's published vectors. Same architecture, same loss, same corpus, same classifier, so the gap
looks like the value of the warm start. It is not, because the fine-tune also runs at a lower
learning rate for fewer epochs, and that gap mixes initialisation with the optimiser schedule.

So I ran the missing control: the same architecture with the fine-tune's exact schedule and a
random start. It scores 0.665 against the fine-tune's 0.792. The warm start is worth 0.127, not
the 0.031 the loose comparison suggested, because the more aggressive schedule had been partly
compensating for the random initialisation. The control is the lowest number in the results table
and it is reported there, since hiding it would defeat the point of running it.

## Good at the task, empty of structure

The three models trained only on movie reviews score between 0.729 and 0.761 on sentiment, within
five points of vectors trained on a hundred billion tokens of news. They also score essentially
zero against human similarity judgements: 0.029, -0.036 and 0.005 Spearman on WordSim-353. One of
them is slightly negative on two of three benchmarks.

Averaging word vectors for a sentiment classifier only needs sentiment-bearing words to occupy
consistent directions. It does not need `tiger` near `cat`. PCA and t-SNE projections, analogy
accuracy, and nearest-neighbour lists all agree with the similarity scores and disagree with the
accuracy scores. `king - man + woman` returns `queen` for the pretrained and fine-tuned models and
returns nothing meaningful for the three trained here.

That is the result I would keep if I had to keep one. Evaluating only on the downstream task would
have produced a confident and wrong conclusion about what these embeddings know.

## Writing the algorithm

The from-scratch implementation covers the parts that are easy to read past in a paper:
subsampling of frequent words, the noise distribution raised to 0.75, a dynamic context window,
and the two embedding matrices where only one survives training.

Its first version did not learn at all. The loss sat at exactly 1.3863 for ten epochs, which is
2 ln 2, the loss of a model whose every logit is zero. The cause was the loss reduction rather
than the sampling: averaging over the batch and over the negatives left an effective per-pair
learning rate near 3e-6, and the measured gradient norm on the input matrix was exactly zero.
Writing the objective from the paper directly, summing over negatives and averaging only over the
batch, fixed it.

I had predicted the opposite failure in my notes beforehand, the one where the loss falls smoothly
and the vectors are garbage. Both are caught by the same discipline of judging on neighbour quality
rather than on the loss curve, but I had guessed the wrong bug.

## Measured rather than assumed

Query latency is linear in vocabulary, as brute-force nearest-neighbour search should be: the
500,000-word model is 37 times slower per query than the 14,309-word one at 35 times the
vocabulary. The GPU is slower than the CPU here, because the batch touches nearly every row of a
small matrix and launch overhead dominates. Negation and contrast account for 38 to 45 percent of
every model's errors, including the pretrained one, which makes it a property of averaging rather
than of embedding quality.

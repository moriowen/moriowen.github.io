---
title: Word2Vec Lab
meta: PyTorch, gensim, Python
featured: true
order: 2
summary: >-
  Five ways to get a Word2Vec model, and eight sets of vectors once three of them are retrained
  on Wikipedia, all scored through one untuned classifier so every difference comes from the
  embeddings. Includes skip-gram with negative sampling written from scratch, a control run that
  corrected the project's own headline claim, and a second corpus that showed similarity and
  sentiment are separate problems.
external:
  - label: Live
    href: https://word2vec-lab.vercel.app/
  - label: Code
    href: https://github.com/moriowen/word2vec-lab
bullets:
  - Compared skip-gram and CBOW in gensim, skip-gram with negative sampling written from scratch in PyTorch, GoogleNews-300 frozen, and GoogleNews fine-tuned, all on 633,720 tokens of the Stanford Sentiment Treebank. Every model runs through one logistic regression that is never tuned per model.
  - Isolated what a pretrained warm start is worth by adding a control matched on learning rate and epochs. It adds +0.127 test accuracy, 0.664 to 0.792, four times what the uncontrolled comparison implied.
  - Retrained the three from-scratch models on 17 million tokens of Wikipedia. Word similarity went from none to near GoogleNews (WordSim-353 Spearman 0.029 to 0.694), while sentiment accuracy fell from 0.761 to 0.722.
---

## What it is

Word2Vec is two matrices and a dot product, which makes it small enough to implement and still
large enough to ask real questions of. I built five variants: skip-gram and CBOW in gensim,
skip-gram written from scratch in PyTorch, Google's pretrained GoogleNews vectors, and those same
vectors fine-tuned on movie reviews. I scored all of them the same way: look up a vector per word,
average into a sentence vector, fit logistic regression, and test on the same 1,821 held-out
sentences. The classifier never changes and is never tuned per model, so any gap between the
numbers belongs to the embeddings.

The three models I trained myself then ran a second time on text8, 17 million tokens of
Wikipedia, with every hyperparameter unchanged. That makes eight sets of vectors in the main
comparison.

## The control that changed the answer

The obvious comparison is the model I trained from scratch against the one warm-started from
Google's published vectors. Same architecture, same loss, same corpus, same classifier, so the gap
looks like the value of the warm start. It is not, because the fine-tune also runs at a lower
learning rate for fewer epochs, and that gap mixes initialisation with the optimiser schedule.

So I ran the missing control: the same architecture with the fine-tune's exact schedule and a
random start. It scores 0.664 against the fine-tune's 0.792. The warm start is worth 0.127, not
the 0.031 the loose comparison suggested, because the more aggressive schedule had been partly
compensating for the random initialisation. The control is the lowest number in the results table
and it is reported there, since hiding it would defeat the point of running it.

## Good at the task, empty of structure

The three models trained only on movie reviews score between 0.729 and 0.761 on sentiment, within
seven points of vectors trained on a hundred billion tokens of news. They also score essentially
zero against human similarity judgements: 0.029, -0.036 and 0.005 Spearman on WordSim-353. One of
them is slightly negative on two of three benchmarks.

Averaging word vectors for a sentiment classifier only needs sentiment-bearing words to occupy
consistent directions. It does not need `tiger` near `cat`. PCA and t-SNE projections, analogy
accuracy, and nearest-neighbour lists all agree with the similarity scores and disagree with the
accuracy scores. `king - man + woman` returns `queen` for the pretrained and fine-tuned models and
returns `scorpion`, `sugar` and `middle-aged` for the three trained on reviews.

Evaluating only on the downstream task would have produced a confident and wrong conclusion
about what these embeddings know.

## More text fixes similarity, not sentiment

If the problem is too little text, more text should fix it. On text8, 27 times the review corpus,
WordSim-353 rises from 0.029 to 0.694 for skip-gram, from -0.036 to 0.666 for CBOW, and from 0.005
to 0.644 for my own implementation, against 0.700 for GoogleNews. Analogy accuracy goes from
almost zero to between 0.31 and 0.37, and all three answer `queen`.

Sentiment accuracy goes the other way. Skip-gram falls from 0.761 to 0.722 and my implementation
from 0.744 to 0.715. Part of that is vocabulary: text8 has no apostrophes, so `n't` is missing,
and it appears in 129 of the 1,821 test sentences. Review words like `soggy`, `sappy` and
`clunker` are missing too. A second measurement fits the rest. When I check whether positive and
negative words form separate groups, the Wikipedia vectors separate them worse than any other
model, which is what you would expect from a corpus that uses `good` and `bad` in the same kinds
of sentence. Wikipedia teaches what words mean. Reviews teach which words praise and which
criticise, and the sentiment test rewards the second.

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

The text8 run needed one change. Dense Adam updates every row of a 135,335-word matrix on every
step, so that run uses sparse Adam, which touches only the rows in the batch. It trained on an
A100 on Georgia Tech's PACE cluster, checkpointing after each epoch so a killed job could resume.

## Measured rather than assumed

A hyperparameter sweep with three seeds per setting showed the headline gap between skip-gram and
CBOW was half noise: 0.032 in single runs, 0.015 averaged over seeds. Architecture matters and the
loss does not; swapping negative sampling for hierarchical softmax moves accuracy by at most
0.002.

Query latency grows with vocabulary, as brute-force nearest-neighbour search should: the
500,000-word model is about 50 times slower per query at the median than the 14,309-word one, at
35 times the vocabulary. On the small vocabulary the laptop GPU is slower than the CPU, because
each batch touches nearly every row of a small matrix and launch overhead dominates. Negation and
contrast account for 37 to 45 percent of every model's errors, including the pretrained one, which
makes it a property of averaging rather than of embedding quality.

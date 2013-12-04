"""
  Copyright 2013 Travis Brady All Rights Reserved.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

Python port of Mikolov's word2phrase.c
From: http://word2vec.googlecode.com/svn/trunk/word2phrase.c
"""
from __future__ import division
from itertools import tee, izip_longest
from collections import defaultdict

def pairwise(iterable):
    """
    Adjacent pairs with overlap
    >>> list(pairwise(range(5)))
    [(0, 1), (1, 2), (2, 3), (3, 4), (4, None)]
    """
    a, b = tee(iterable)
    next(b)
    return izip_longest(a, b)

def learn_vocab_from_train_iter(train_iter):
    """
    Creates a frequency table mapping unigrams and bigrams to their
    count of appearances in the training set
    Analogous to LearnVocabFromTrainFile from original
    """
    vocab = defaultdict(int)
    train_words = 0
    for line in train_iter:
        for pair in pairwise(line):
            vocab[pair[0]] += 1
            if None not in pair:
                vocab[pair] += 1
            train_words += 1
    return vocab, train_words

def filter_vocab(vocab, min_count):
    """
    Filter elements from the vocab occurring fewer than min_count times
    """
    return dict((k, v) for k, v in vocab.iteritems() if v >= min_count)

def train_model(train_iter, min_count=5, threshold=100.0, sep='_'):
    """
    The whole file-to-file (or in this case iterator to iterator) enchilada
    Does the same thing as Mikolov's original TrainModel in word2phrase.c
    Parameters:
    train_iter : an iterator containing tokenized documents
        Example: [['hi', 'there', 'friend'],['coffee', 'is', 'enjoyable']]
    min_count : min number of mentions for filter_vocab to keep word
    threshold : pairs of words w/ score >= threshold are marked as phrases.
        In word2phrase.c this meant the whitespace separating
        two words was replaced with '_'

    Yields:
        One list per row in input train_iter
    """
    vocab_iter, train_iter = tee(train_iter)
    vocab, train_words = learn_vocab_from_train_iter(vocab_iter)
    print "Done Vocab", len(vocab), train_words
    vocab = filter_vocab(vocab, min_count)
    print "Filtered Vocab", len(vocab)

    for line in train_iter:
        out_sentence = []
        pairs = pairwise(line)
        for pair in pairs:
            pa = vocab.get(pair[0])
            pb = vocab.get(pair[1])
            pab = vocab.get(pair)

            if all((pa, pb, pab)):
                score = (pab - min_count) / pa / pb * train_words
            else:
                score = 0.0
            if score > threshold:
                next(pairs)
                out_sentence.append(sep.join(pair))
            else:
                out_sentence.append(pair[0])
        yield out_sentence

def main():
    """
    When called as a script this mimics the original word2phrase.c
    With a couple exceptions:
        1. We don't truncate words to 60 chars as in the original
        2. Whitespace handling doesn't exactly match the original
    """
    from optparse import OptionParser
    p = OptionParser()
    p.add_option('--train', dest='train_file', help='Input file')
    p.add_option('--output', dest='output_file', help='Output file')
    p.add_option('--min-count', type="int", dest='min_count', default=5)
    p.add_option('--threshold', type="float", dest='threshold', default=100.0)
    p.add_option('--sep', dest='sep', default='_', help='Character used to separate phrases')
    p.add_option('--iters', type='int', dest='iters',
                 default=1, help='Number of times to run train_model. More runs = longer phrases')
    p.add_option('--threshold-discount', type='float',
                 dest='discount', default=0.05,
                 help='% of initial value by which to decrement threshold with each iter')
    (options, _) = p.parse_args()

    train_file = (line.split() for line in file(options.train_file))
    out = train_file
    for i in range(options.iters):
        this_thresh = max(options.threshold - (i * options.discount * options.threshold), 0.0)
        print "Iteration: %d Threshold: %6.2f" % (i, this_thresh)
        out = train_model(out, min_count=options.min_count,
                threshold=this_thresh,
                sep=options.sep)
    out_fh = open(options.output_file, 'w')
    for row in out:
        out_fh.write(' '.join(row) + '\n')
    out_fh.close()

if __name__ == '__main__':
    main()


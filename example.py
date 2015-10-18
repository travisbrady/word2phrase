"""
A simple example using word2phrase to find multiword phrases.
Runs word2phrase passes over text from Pride and Prejudice
and then prints the most common 2 and 3 word phrases to stdout
Requires textblob for tokenization
Author: Travis Brady 2015-10-18
"""
import word2phrase
from textblob import TextBlob
from collections import Counter


def get_book():
    book_txt = open('pride_and_prejudice.txt').read().decode('utf-8')
    book_tb = TextBlob(book_txt.lower())
    return [s.words for s in book_tb.sentences if s]


def main():
    book_sentences = get_book()
    phrased1 = word2phrase.train_model(book_sentences, min_count=3)
    phrased2 = word2phrase.train_model(phrased1, min_count=3)
    two_word_counter = Counter()
    three_word_counter = Counter()
    for sentence in phrased2:
        for word in sentence:
            if word.count('_') == 1:
                two_word_counter[word] += 1
            if word.count('_') == 2:
                three_word_counter[word] += 1

    print '=' * 60
    print 'Top 20 Two Word Phrases'
    for phrase, count in two_word_counter.most_common(20):
        print '%56s %6d' % (phrase, count)

    print
    print '=' * 60
    print 'Top 10 Three Word Phrases'
    for phrase, count in three_word_counter.most_common(10):
        print '%56s %6d' % (phrase, count)


if __name__ == '__main__':
    main()

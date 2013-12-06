'''
Quick script to learn the vocab and dump it out as a file
File format is strange and non-standard SORRY
Format:
    First row = train_words : Long
    All other rows = {"w": "word", "c": 123}
'''
from sys import stdin, argv
from collections import Counter
from json import dumps

MAX_VOCAB = 10000000

def main():
    min_count = int(argv[1])
    ctr = Counter()
    train_words = 0
    for line in stdin:
        words = line.split()
        train_words += len(words)
        ctr.update(words)
        ctr.update([x+"_"+y for x,y in zip(words, words[1:])])

    print train_words
    for k,ct in ctr.most_common(MAX_VOCAB):
        if ct < min_count:
            break
        print dumps(dict(w=k, c=ct))

if __name__ == '__main__':
    main()


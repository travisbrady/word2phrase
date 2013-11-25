from sys import stdin, argv
from collections import Counter

try:
    k = int(argv[1])
except:
    k = 10

ctr = Counter()
for line in stdin:
    words = line.strip().split()
    ctr.update(words)

for k, v in ctr.most_common(k):
    print v, k


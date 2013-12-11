import re
from sys import stdin
from json import loads
from pybloom import BloomFilter
from HTMLParser import HTMLParser
hp = HTMLParser()

bloom = BloomFilter(capacity=100000000)

for line in stdin:
    j = loads(line)
    s = j['text']
    s = hp.unescape(s)
    s = s.lower()
    s = s.replace("'", '')
    s = s.replace('_', ' ')
    s = s.replace("\n", " ")
    s = re.sub(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', ' URL ', s)
    s = re.sub(r'(^|[^@\w])@(\w{1,15})\b', ' USER ', s)
    s = re.sub(r'[^\w\s]', ' ', s)
    s = re.sub('happ+y', ' happy ', s)
    s = re.sub('crazy+', ' crazy ', s)
    s = re.sub('lmao+', ' lmao ', s)
    s = re.sub('lmfao+', ' lmfao ', s)
    s = re.sub(' fu+ck ', ' fuck ', s)
    s = re.sub(' shi+t ', ' shit ', s)
    s = re.sub(' +', ' ', s)
    if len(s) > 4 and 'gameinsight' not in s:
        if s[0] == ' ':
            s = s[1:]
        if s not in bloom:
            bloom.add(s)
            print s

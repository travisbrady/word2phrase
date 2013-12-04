import re
from sys import stdin

for line in stdin:
    s = line.lower()
    s = s.replace("'", '')
    s = re.sub(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', ' URL ', s)
    s = re.sub(r'(^|[^@\w])@(\w{1,15})\b', ' USER ', s)
    s = re.sub(r'[^\w\s]', ' ', s)
    s = re.sub('happ+y', ' happy ', s)
    s = re.sub('crazy+', ' crazy ', s)
    s = re.sub('lmao+', ' lmao ', s)
    s = re.sub('lmfao+', ' lmfao ', s)
    s = re.sub(' +', ' ', s)
    if len(s) > 4 and 'gameinsight' not in s:
        if s[0] == ' ':
            s = s[1:]
        print s,

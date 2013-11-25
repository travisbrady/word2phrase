word2phrase
===========

Python port of Mikolov's word2phrase.c from the word2vec toolkit

Given a document or documents this program attempts to learn phrases.

Example using the text8 corpus used in Mikolov's experiments:
```
$ time python word2phrase.py --train=text8 --output=text8-phrase-py --min-count=5 --threshold=500.0
# Now count instances of phrases.  We separate phrases with an underscore
$ cat text8-phrase-py| tr ' ' '\n' | grep '_' | python wordcount.py 20
9913 united_states
7100 th_century
6761 external_links
4942 new_york
3147 rather_than
2371 united_kingdom
2184 prime_minister
1602 soviet_union
1507 civil_war
1464 main_article
1266 no_longer
1247 science_fiction
1100 don_t
1095 new_zealand
1069 hong_kong
1067 http_www
1019 north_america
998 los_angeles
959 roman_catholic
940 air_force
```

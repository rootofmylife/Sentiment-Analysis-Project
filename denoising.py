from collections import Counter, OrderedDict
from pyvi.pyvi import ViTokenizer
import re

class OrderedCounter(Counter, OrderedDict):
	pass

with open('comment.txt', encoding='utf-8') as f:
	cmt = f.read().splitlines()

cmt = [s.replace('\t',' ') for s in cmt]
email_regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
phone_regex = r"\(?(01[2689]|09)\)?([\W ]?([0-9])){8}"

sym = r"~`!@#$%^&*()-+=[]{}|;':\"”“,./<>?–"
cmt = list(set(cmt))

cmt = [re.sub("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", ' <EMAIL_HOLDER> ', i) for i in cmt]

cmt = [re.sub(phone_regex, ' <PHONE_HOLDER> ', i) for i in cmt]

#for i in cmt:
#	if '<EMAIL_HOLDER>' in i or '<PHONE_HOLDER>' in i:
#		print(i)
		
cmt = [ViTokenizer.tokenize(s).lower() for s in cmt]
cmt = [s.translate({ord(c): "" for c in sym}) for s in cmt]
cmt = ' '.join(cmt)
cmt = cmt.split()
cmt_word = OrderedCounter(cmt)
print(cmt_word.most_common(50))
print(len(cmt_word))

output = open('vocab.txt', 'w')
for i in range(len(cmt_word)):
	output.write(i[0][0] + ': ' + i[0][1])
	output.write('\n')

output.close()

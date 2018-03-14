from collections import Counter, OrderedDict
from pyvi.pyvi import ViTokenizer
import re

class OrderedCounter(Counter, OrderedDict):
	pass

with open('comment.txt', encoding='utf-8') as f:
	cmt = f.read().splitlines()



cmt = [s.replace('\t',' ') for s in cmt]
email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

sym = r"~`!@#$%^&*()-+=[]{}|;':\"”“,./<>?–_"
cmt = list(set(cmt))

cmt = [re.sub("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", '<EMAIL_HOLDER>', i) for i in cmt]

for i in cmt:
	if '<EMAIL_HOLDER>' in i:
		print(i)
	#test_email = re.search(email_regex, i)
	#if test_email:
		#test = re.sub("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", '<EMAIL_HOLDER>', i)
		print(i)
		#print(test_email.group(1))
		#cmt[i] = cmt[i].replace(test_email.group(1), "<EMAIL_HOLDER>")
		#print(cmt[i])
		
#cmt = [ViTokenizer.tokenize(s).lower() for s in cmt]
#cmt = [s.translate({ord(c): "" for c in sym}) for s in cmt]
#cmt = ' '.join(cmt)
#cmt = cmt.split()
#cmt_word = OrderedCounter(cmt)
#print(cmt_word.most_common(50))
#print(len(cmt_word))

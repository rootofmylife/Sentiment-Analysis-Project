import re
from pyvi.pyvi import ViTokenizer

with open('comment.txt', encoding='utf-8') as f:
	mess = f.read().splitlines()

with open('key.txt', encoding='utf-8') as fk:
	keys = fk.read().splitlines()

# xóa các ký tự k quan trọng, còn thiếu URL
email_regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
phone_regex = r"\(?(01[2689]|09|028)\)?([\W ]?([0-9])){8}"
sym = r"~`!@#$%^&*()_-+=[]{}|;':\"”“,./<>?"
mess = [re.sub("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", ' <EMAILxHOLDER> ', i) for i in mess]
mess = [re.sub(phone_regex, ' <PHONExHOLDER> ', i) for i in mess]
# xây lại bộ tách từ cho informal words, tạm thời thì dùng cái này
# https://www.semanticscholar.org/search?q=Vietnamese%20Word%20Segmentation&sort=relevance&pdf=true&fos=computer-science
cmt = [ViTokenizer.tokenize(s).lower() for s in cmt] # tách từ
#################################
keys = [s.translate({ord(c): " " for c in sym}) for s in keys]
mess = [s.translate({ord(c): " " for c in sym}) for s in mess]
mess = [s.replace('\t', ' ').replace('\n', ' ') for s in mess]
mess = [s.strip() for s in mess if s != 'NULL']
mess = [s for s in mess if len(s) != 0]
keys = [s.lower() for s in keys]
mess = list(set(mess)) # bỏ các câu trùng, chỉ áp dụng với cmt, k áp dụng với mess

# tìm từ sai của từ khóa, dùng n-gram hoặc nltk

# tạo từ điển
vocab = ' '.join(mess) # tạo từ điển
vocab = vocab.split() # tạo từ điển
one_vocab = list(set(vocab)) # từ điển k có từ trùng, từ lặp lại

# đếm tần số xuất hiện của từ
fre_vocab = {}
for v in vocab:
	if v not in fre_vocab:
		fre_vocab[v] = 1
	else:
		fre_vocab[v] += 1
sorted_vocab = sorted(fre_vocab.items(), key=lambda x: x[1], reverse=True)

# xuất file tần số các từ
# fre_output = open('fre_word.txt', 'w')
# for t in sorted_vocab:
#    fre_output.write(str(t[0]) + ': ' + str(t[1]))
#    fre_output.write('\n')
# fre_output.close()

# bỏ từ 2 biên, rút gọn xuống 1000 từ, tránh các từ key word

# gán NER: PER, ORG, LOC
# (7 class:	Location, Person, Organization, Money, Percent, Date, Time)

# Rút gọn câu (Denoising Encoder)

# tạo và xuất corpus cho glove (wor2vec)
# glove = ' '.join(vocab)
# cor = open('corpus.txt', 'w')
# cor.write(glove)
# cor.close()
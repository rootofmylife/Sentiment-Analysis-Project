import re
from pyvi import ViTokenizer
import nltk

with open('comment.txt', encoding='utf-8') as f:
	mess = f.read().splitlines()

with open('key.txt', encoding='utf-8') as fk:
	keys = fk.read().splitlines()

# xóa các ký tự k quan trọng
email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
# email_regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
phone_regex = r"\(?(01[2689]|09|028)\)?([\W ]?([0-9])){8}"
sym = r"~`!@#$%^&*()_-+=[]{}|;':\"”“,./<>?"
url_regex = r'(\w+:\/{2})?[\d\w-]+(\.[\d\w-]+)+(?:(?:\/[^\s/]*))*'
mess = [re.sub(email_regex, ' <EMAILxHOLDER> ', i) for i in mess]
mess = [re.sub(phone_regex, ' <PHONExHOLDER> ', i) for i in mess]
mess = [re.sub(url_regex, ' <URLxHOLDER> ', i) for i in mess]
# xây lại bộ tách từ cho informal words, tạm thời thì dùng cái này
# https://www.semanticscholar.org/search?q=Vietnamese%20Word%20Segmentation&sort=relevance&pdf=true&fos=computer-science
mess = [ViTokenizer.tokenize(s).lower() for s in mess] # tách từ
#################################
keys = [s.translate({ord(c): " " for c in sym}) for s in keys]
mess = [s.translate({ord(c): " " for c in sym}) for s in mess]
mess = [s.replace('\t', ' ').replace('\n', ' ') for s in mess]
mess = [s.strip() for s in mess if s != 'NULL']
mess = [s for s in mess if len(s) != 0]
keys = [s.lower() for s in keys]
mess = list(set(mess)) # bỏ các câu trùng, chỉ áp dụng với cmt, k áp dụng với mess, có nên dùng với glove k?

# tạo từ điển
vocab = ' '.join(mess) # tạo từ điển
vocab = vocab.split() # tạo từ điển
one_vocab = list(set(vocab)) # từ điển k có từ trùng, từ lặp lại

# tìm từ sai của từ khóa
vob_key = ' '.join(keys) # tạo từ điển cho keyword
vob_key = keys.split()
vob_key = list(set(vob_key)) # trành TH trùng, lặp từ
key_with_miss = {}

for k in vob_key:
	set_k = []
	for m in one_vocab:
		if k in m:
			set_k.append(m)
		temp_dv = nltk.edit_distance(k.lower(), m.lower())	
		if temp_dv < (len(k) - (len(k) * 0.5)) and temp_dv > 0:
			set_k.append(m)
		# if sentenceAlignment(k, m) <= 0 and sentenceAlignment(k, m) >= -4:
		# 	set_k.append(m)
	key_with_miss[k] = set_k

# kiểm tra câu chứa từ sai do các tổ hợp từ sai tạo ra
sent_with_miss = []
for k in keys:
	this_sent = ''
	split_key = k.split() # từ 1 từ tách thành nhiều từ
	for sk in range(len(split_key)):
		this_sent = key_with_miss[split_key[0]][sk] # bắt đầu với từ đầu tiên
		it = 1
		while it < len(split_key): # dò từng key của từ khóa
			qk = 0
			while True:
				this_sent += ' ' + key_with_miss[split_key[it]][qk]
				if qk == len(key_with_miss[split_key[len(split_key) - 1]]): # lấy chữ cuối cùng của keyqord
					break
				if qk != len(split_key):
					break
				else:
					for m in mess:
						if this_sent in mess:
							sent_with_miss.append(mess)
				qk += 1
			it += 1	

# thay keywork and notmatch-keyword bằng KEYWORD_(1->n), giảm chiều vector

# dùng n-gram để dự đoán những từ k có trong corpus nhưng có thể xuất hiện (làm sau)

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

# gán NER: PER, ORG, LOC
# (7 class:	Location, Person, Organization, Money, Percent, Date, Time)
# cần train lại trên tập dữ liệu sai

# bỏ từ 2 biên, rút gọn xuống 1000 từ, tránh các từ key word
# muốn bỏ các từ k cần thiết cần sd các hàm reduction dimension
# nếu chỉ cắt 2 biên thì rất dễ bỏ những từ có nghĩa (do viết sai)
# bỏ các từ dài hơn 9 kí tự, xóa từ chứa kí hiệu lạ
person_noun = ['tôi', 'tao', 'ta', 'tớ', 'mình', 'chúng tôi', 'chúng ta', 'chúng tớ', 'chúng tao', 'chúng mình',
				'bạn', 'các bạn', 'đằng ấy', 'mày', 'bọn mày', 'tên kia', 'lũ', 'đám', 'bây',
				'anh ấy', 'cậu ấy', 'ông ấy', 'gã ấy', 'y', 'hắn',
				'cô ấy', 'chị ấy', 'bà ấy', 'ả', 'thị', 'cổ', 'ấy',
				'nó', 'chúng nó', 'họ', 'ông', 'bà', 'cụ', 'cố',
				'thím', 'bác', 'chú', 'dì', 'cô', 'mợ', 'dượng', 'thầy', 'cậu',
				'thằng', 'thằng chó', 'đấng', 'thánh',
				'mẹ', 'má', 'cha', 'ba', 'u', 'con', 'anh', 'chị', 'tía', 'bu', 'bầm',
				'ad', 'admin', 'assmin']

# Rút gọn câu (Denoising Encoder)
# Feature Cleaning, Feature Imputation, Feature Engineering, Feature Selection, Feature Normalization or Scaling

# tạo và xuất corpus cho glove (wor2vec)
# glove = ' '.join(vocab)
# cor = open('corpus.txt', 'w')
# cor.write(glove)
# cor.close()
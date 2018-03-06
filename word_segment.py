from pyvi.pyvi import ViTokenizer, ViPosTagger
#from polyglot.text import Text
from collections import Counter, OrderedDict
#import warnings
#warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

#from gensim.models import TfidfModel
# Xử lý kém câu "học sinh học sinh học", cần chú ý khi tách từ trong sentiment

class OrderedCounter(Counter, OrderedDict):
    pass

with open('mess.txt', encoding='utf-8') as f:
    mess = f.read().splitlines()

with open('stopwords.txt', encoding='utf-8') as fw:
    stopword = fw.read().splitlines()
'''
Bước 1: tách aspects
'''
mess = set(mess)
mess1 = list(mess)
mess1 = [ViTokenizer.tokenize(i) for i in mess1]

# đã bỏ _
sym = r"~`!@#$%^&*()-+=[]{}|;':\"”“,./<>?–"

mess1 = [s.translate({ord(c): "" for c in sym}) for s in mess1]	

print(len(mess1)) # câu đã bỏ giống nhau

mess1 = ' '.join(mess1) 
mess1 = mess1.split()

print(len(mess1)) # từ chưa bỏ giống nhau
print(len(set(mess1))) # từ bỏ giống nhau

# https://stackoverflow.com/questions/20510768/count-frequency-of-words-in-a-list-and-sort-by-frequency
# https://gist.github.com/bradmontgomery/4717521
# https://stackoverflow.com/questions/35071619/python-counter-keys-return-values
tokenized_word = OrderedCounter(mess1) # tìm tần số mỗi từ
most_common_words = tokenized_word.most_common(100) # lấy ra các từ có tần số cao nhất

# tìm những từ chung nhất dựa trên tần số
later_words = []
for w in most_common_words:
    if w[0] not in stopword:
        later_words.append(w[0])

# tìm những câu chứa những từ này (loại bỏ stop words)
words_in_sent = []
for m in mess:
    for w in later_words:
        if w in m:
            words_in_sent.append(m)

words_in_sent = list(set(words_in_sent))
print(len(words_in_sent)) # các câu chứa các từ có tần số xuất hiện nhiều
print(len(later_words))
# tách ra noun và noun phrase bằng dùng POS, từ những câu đã tìm ở trên
# xử lý dc 2 chuỗi song song, tách dc noun và noun phrase, dc thì tách lun sentiment (chưa khả thi)

POS_sent = words_in_sent[0:10]

for p in POS_sent:
    print(ViPosTagger.postagging(ViTokenizer.tokenize(p)))



'''
Bước 2: đánh giá sentiment
'''
# đánh giá câu dựa trên những sentiments có sẵn
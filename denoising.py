from collections import Counter, OrderedDict
from pyvi.pyvi import ViTokenizer
import re
import operator

with open('comment.txt', encoding='utf-8') as f:
	cmt = f.read().splitlines()

cmt = [s.replace('\t',' ') for s in cmt]
email_regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
phone_regex = r"\(?(01[2689]|09)\)?([\W ]?([0-9])){8}"

sym = r"~`!@#$%^&*()-+=[]{}|;':\"”“,./<>?–"
cmt = list(set(cmt)) # bỏ các câu trùng

cmt = [re.sub("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", ' <EMAIL_HOLDER> ', i) for i in cmt]
cmt = [re.sub(phone_regex, ' <PHONE_HOLDER> ', i) for i in cmt]
cmt = [ViTokenizer.tokenize(s).lower() for s in cmt] # tách từ
cmt = [re.sub("[^a-zA-Z0-9~`!@#$%^&*()-+=[]{}|;':\"”“,./<>?–_]", ' <SYMBOL> ', i) for i in cmt]
cmt = [s.translate({ord(c): "" for c in sym}) for s in cmt] # bỏ symbol
sent = cmt
cmt = ' '.join(cmt) # tạo từ điển
cmt = cmt.split() # tạo từ điển
print(len(set(cmt)))
cmt = ' '.join(cmt)
# tạo corpus cho glove
cor = open('corpus.txt', 'w')
cor.write(cmt)
cor.close()
######################
##############################################################################
# đếm số lần xuất hiện của 1 từ
#vocab = {}

#for v in cmt:
#	if v not in vocab:
#		vocab[v] = 0
#	else:
#		vocab[v] += 1
#sorted_vocal = sorted(vocab.items(), key=lambda x: x[1], reverse=True)
##############################################################################
'''
cmt = set(cmt)
word2int = {}
int2word = {}
vocab_size = len(cmt)
for i,word in enumerate(cmt):
    word2int[word] = i
    int2word[i] = word

# tách câu
sentences = []
for sentence in sent:
    sentences.append(sentence.split())

# tách câu thành cặp từ
WINDOW_SIZE = 2
data = []
for sentence in sentences:
    for word_index, word in enumerate(sentence):
        for nb_word in sentence[max(word_index - WINDOW_SIZE, 0) : min(word_index + WINDOW_SIZE, len(sentence)) + 1] : 
            if nb_word != word:
                data.append([word, nb_word])

# function to convert numbers to one hot vectors
def to_one_hot(data_point_index, vocab_size):
    temp = np.zeros(vocab_size)
    temp[data_point_index] = 1
    return temp

x_train = [] # input word
y_train = [] # output word

for data_word in data:
    x_train.append(to_one_hot(word2int[ data_word[0] ], vocab_size))
    y_train.append(to_one_hot(word2int[ data_word[1] ], vocab_size))

# convert them to numpy arrays
x_train = np.asarray(x_train)
y_train = np.asarray(y_train)

# making placeholders for x_train and y_train
x = tf.placeholder(tf.float32, shape=(None, vocab_size))
y_label = tf.placeholder(tf.float32, shape=(None, vocab_size))

EMBEDDING_DIM = 5 # you can choose your own number
W1 = tf.Variable(tf.random_normal([vocab_size, EMBEDDING_DIM]))
b1 = tf.Variable(tf.random_normal([EMBEDDING_DIM])) #bias
hidden_representation = tf.add(tf.matmul(x,W1), b1)

W2 = tf.Variable(tf.random_normal([EMBEDDING_DIM, vocab_size]))
b2 = tf.Variable(tf.random_normal([vocab_size]))
prediction = tf.nn.softmax(tf.add( tf.matmul(hidden_representation, W2), b2))

sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init) #make sure you do this!

# define the loss function:
cross_entropy_loss = tf.reduce_mean(-tf.reduce_sum(y_label * tf.log(prediction), reduction_indices=[1]))

# define the training step:
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cross_entropy_loss)

n_iters = 10000
# train for n_iter iterations

for _ in range(n_iters):
    sess.run(train_step, feed_dict={x: x_train, y_label: y_train})
    print('loss is : ', sess.run(cross_entropy_loss, feed_dict={x: x_train, y_label: y_train}))

vectors = sess.run(W1 + b1)

def euclidean_dist(vec1, vec2):
    return np.sqrt(np.sum((vec1-vec2)**2))

def find_closest(word_index, vectors):
    min_dist = 10000 # to act like positive infinity
    min_index = -1
    query_vector = vectors[word_index]
    for index, vector in enumerate(vectors):
        if euclidean_dist(vector, query_vector) < min_dist and not np.array_equal(vector, query_vector):
            min_dist = euclidean_dist(vector, query_vector)
            min_index = index
    return min_index
'''
# f = open('vocab.txt', 'w')
# for t in sorted_vocal:
#    f.write(str(t[0]) + ': ' + str(t[1]))
#    f.write('\n')
# f.close()

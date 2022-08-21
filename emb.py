
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer
from nltk import corpus, SnowballStemmer
from string import punctuation
from gensim.models.fasttext import FastText

#https://www.kaggle.com/datasets/fabiochiusano/medium-articles


def spliting(a):
    pun = list(punctuation)

    ss = SnowballStemmer('english')
    # spiliting a sentences
    text = sent_tokenize(a)
    text_list = []
    #spiliting a word in a sentence
    for ii in text:
        text_ = word_tokenize(ii)
        for i in text_:
            #removing the useless words for the sentence
            if i not in corpus.stopwords.words('english'):
                if i not in pun:
                    word = ss.stem(i)
                    text_list.append(word) #envolving every word of sentences in same list
    imp_text = ' '
    tet = imp_text.join(text_list)

    return tet

fil = pd.read_csv('dataset/articles_tags/medium_articles.csv')

fil.sample(n=300, replace='False')

title = fil['title']
text = fil['text']

num = 700

all_words = []

for tit in range(0, num):
    word = word_tokenize(title[tit])
    all_words.append(word)

    text1 = spliting(text[tit])
    word = word_tokenize(text1)
    all_words.append(word)


context_window = 20
vector_size = 1
min_word_count = 1
sample = 1e-3
sg = 1
fast_text_model = FastText(all_words,
window=context_window, min_count=min_word_count, sg=sg,
 sample=sample, vector_size=vector_size
)


def word_embedding(word):
    return fast_text_model.wv[word]

import feedparser

import tensorflow as tf
import numpy as np
from transformers import *

import re, string
import pandas as pd

import sys

from keras.preprocessing.sequence import pad_sequences

feed = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml')
titles = [article.title for article in feed.entries]

print(f'Number of titles: {len(titles)}')

tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

original_titles = titles.copy()
titles = [tokenizer.tokenize('[CLS] ' + title + ' [CEP]') for title in titles] 

MAX_LEN=128

input_ids = pad_sequences([tokenizer.convert_tokens_to_ids(title) for title in titles],
        maxlen=MAX_LEN, dtype='long', truncating='post', padding='post')

model = TFBertForSequenceClassification.from_pretrained('./seemsaccurate6/')
classes = ['negative', 'positive']
results = model.predict(input_ids)

count_g = 0
total_g = 0

countp = 0
countn = 0

def print_accuracy(count, total):    
    accuracy = (count / total) * 100
    print(f'Total articles: {total}')
    print(f'Total correct: {count}')
    print('Accuracy {:.2f}'.format(accuracy))

for i in range(len(results)):
    classi = np.argmax(results[i])
    title = original_titles[i]

    total_g += 1
    '''
    if classi == 1:
        print(title)
        countp += 1

    if classi == 0:
        countn += 1
    '''

    print(title)
    print(f'Class: {classi}')

#    print('**')
#    print(f'Title: {title}')
#    orig_classi = int(input('Human classification: '))

 #   if orig_classi == classi:
 #       count_g += 1
    
 #   print_accuracy(count_g, total_g)
 #   print('**')
print(countp)
print(countn)


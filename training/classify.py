import tensorflow as tf
import numpy as np
from transformers import *

import re, string
import pandas as pd

import sys

from keras.preprocessing.sequence import pad_sequences

def map_sent(sent):
    if sent == 'positive' or sent == 'neutral': 
        return 1
    if sent == 'negative':
        return 0

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
pattern = re.compile('[\W_]+', re.UNICODE)

df = pd.read_csv('dataset/Tweets.csv')

df = df[:5000]

df['text'] = df['text'].apply(lambda title: deEmojify(title))
df['text'] = df['text'].apply(lambda title: re.sub(r"http\S+", "", title))
df['text'] = df['text'].apply(lambda title: ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",title).split()))

df['original'] = df['text'].copy()

df['text'] = df['text'].apply(lambda title: '[CLS] ' + title + ' [CEP]')
df['text'] = df['text'].apply(lambda title: tokenizer.tokenize(title))

df['airline_sentiment'] = df['airline_sentiment'].apply(lambda sent: map_sent(sent))

MAX_LEN=128

input_ids = pad_sequences([tokenizer.convert_tokens_to_ids(title) for title in df['text']],
        maxlen=MAX_LEN, dtype='long', truncating='post', padding='post')

model = TFBertForSequenceClassification.from_pretrained('./seemsaccurate7/')
classes = ['negative', 'positive']
results = model.predict(input_ids)

count = 0
total = 0

for i in range(len(results)):
    classi = np.argmax(results[i])
    orig_sent = df['airline_sentiment'][i]
    confidence = df['airline_sentiment_confidence'][i]

    if confidence == 1:
        total += 1
        if orig_sent == classi:
            count += 1

    print('Sentence: {:s}'.format(df['original'][i]))
    print('Sentiment: {:s}'.format(classes[classi]))
    print('Real Sentiment: {:s}'.format(classes[orig_sent]))

accuracy = (count / total) * 100

print(count)
print(total)
print('Accuracy {:.2f}'.format(accuracy))


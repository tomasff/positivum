import tensorflow as tf
from transformers import *

from keras.preprocessing.sequence import pad_sequences

import keras

import numpy as np
import pandas as pd
import io

def convert_pol(pol):
    if pol == -1:
        return 0
    if pol == 1 or pol == 0:
        return 1

tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

df = pd.read_csv('dataset/processed/titles-bbc-1-classified.csv')

df['title'] = df['title'].apply(lambda title: '[CLS]' + title + '[CEP]')
df['title'] = df['title'].apply(lambda title: tokenizer.tokenize(title))

df['sentiment_polarity'] = df['sentiment_polarity'].apply(lambda pol: convert_pol(pol))

'''
df = pd.read_csv('dataset/train.csv')

df['SentimentText'] = df['SentimentText'].apply(lambda title: '[CLS] ' + title + ' [CEP]')
df['SentimentText'] = df['SentimentText'].apply(lambda title: tokenizer.tokenize(title))
'''
MAX_LEN = 128

input_ids = pad_sequences([tokenizer.convert_tokens_to_ids(title) for title in df['title']],
        maxlen=MAX_LEN, dtype='long', truncating='post', padding='post')

tensorboard_callback = keras.callbacks.TensorBoard(log_dir='logs/')

model = TFBertForSequenceClassification.from_pretrained('bert-base-cased', num_labels=2)
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5, epsilon=1e-08, clipnorm=1.0, amsgrad=True)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

with tf.device('/device:GPU:0'):
    train = model.fit(x=input_ids, y=df['sentiment_polarity'].values, epochs=15,
                        validation_split=0.4, validation_steps=7, verbose=1, batch_size=30, steps_per_epoch=30, callbacks=[tensorboard_callback])

model.save_pretrained('./save/')

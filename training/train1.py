import tensorflow as tf
from transformers import *

from keras.preprocessing.sequence import pad_sequences

import keras

import numpy as np
import pandas as pd
import io

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
'''
df = pd.read_csv('dataset/processed/titles-bbc-1-classified.csv')

df['title'] = df['title'].apply(lambda title: '[CLS]' + title + '[CEP]')
df['title'] = df['title'].apply(lambda title: tokenizer.tokenize(title))
'''
df = pd.read_csv('dataset/train.csv')

df['SentimentText'] = df['SentimentText'].apply(lambda title: '[CLS] ' + title + ' [CEP]')
df['SentimentText'] = df['SentimentText'].apply(lambda title: tokenizer.tokenize(title))

MAX_LEN = 128

input_ids = pad_sequences([tokenizer.convert_tokens_to_ids(title) for title in df['SentimentText']],
        maxlen=MAX_LEN, dtype='long', truncating='post', padding='post')

tensorboard_callback = keras.callbacks.TensorBoard(log_dir='logs/')

model = TFBertForSequenceClassification.from_pretrained('bert-base-cased', num_labels=2)
optimizer = tf.keras.optimizers.Adam(learning_rate=2e-5, epsilon=1e-08, clipnorm=1.0, amsgrad=True)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

with tf.device('/device:GPU:0'):
    train = model.fit(x=input_ids, y=df['Sentiment'].values, epochs=60,
                        validation_split=0.2, validation_steps=7, verbose=1, batch_size=30, steps_per_epoch=30, callbacks=[tensorboard_callback])

model.save_pretrained('./save/')

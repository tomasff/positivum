import feedparser

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from transformers import BertTokenizer, TFBertForSequenceClassification

import numpy as np

import re

from enum import IntEnum

from database import Article, Source

tf.config.set_soft_device_placement(True)

class Classification(IntEnum):
    NEGATIVE = 0
    POSITIVE_NEUTRAL = 1

class Processer:

    def __init__(self, database):
        self.database = database
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
        self.model = TFBertForSequenceClassification.from_pretrained('./model/')
        self.html_regex = re.compile('<.*?>')

    def _clean_html(self, text):
        return self.html_regex.sub(' ', text)

    def _tokenize(self, text):
        tokenized_text = '[CLS] ' + text + ' [CEP]'
        tokenized_text = self.tokenizer.tokenize(tokenized_text)
        
        return tokenized_text

    def _convert_to_ids(self, tokenized_articles):
        ids = pad_sequences([self.tokenizer.convert_tokens_to_ids(article) for article in tokenized_articles],
                maxlen=128, dtype='long', truncating='post', padding='post')

        return ids

    def _shorten_desc(self, desc, length):
        if len(desc) > length:
            return desc[:length-3] + '...'

        return desc

    def _analyze(self, articles):
        tokenized_articles = [self._tokenize(article.title) for article in articles]
        input_ids = self._convert_to_ids(tokenized_articles)

        predictions = self.model.predict(input_ids)
        predictions = [np.argmax(prediction).item() for prediction in predictions]

        return predictions

    def _prepare_article_db(self, article, prediction):
        if 'description' not in article:
            article['description'] = 'No description was provided'

        return Article(title = article.title,
                    description = self._shorten_desc(self._clean_html(article.description), 256),
                    classification = prediction,
                    url = article.link,
                    pub_date = article.published_parsed)

    # TODO: Implement confidence levels
    def process(self):
        with self.database.get_session() as sess:
            sources = sess.query(Source).all()

            for source in sources:
                feed = feedparser.parse(source.feed_url)
                articles = feed.entries

                new_articles = [article for article in articles if not sess.query(Article).filter_by(url=article.link).first()]

                if len(new_articles) == 0:
                    continue

                predictions = self._analyze(new_articles)                
                classified_articles = [self._prepare_article_db(article, prediction) for article, prediction in zip(new_articles, predictions)]
                
                source.articles.extend(classified_articles)


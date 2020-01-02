import feedparser

import re, string
import pandas as pd

import csv

import sys

feed = feedparser.parse('https://www.standard.co.uk/news/world/rss?ito=1588')
titles = [article.title for article in feed.entries]

print(f'Number of titles: {len(titles)}')

classifications = list()

for title in titles:
    print(title)
    classi = int(input('Class: '))

    classifications.append({
        'title': title,
        'sentiment_polarity': classi
    })

with open('standard.csv', 'w') as csv_f:
    writer = csv.DictWriter(csv_f, fieldnames=['title', 'sentiment_polarity'])
    writer.writeheader()
    for data in classifications:
        writer.writerow(data)


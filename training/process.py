import os, shutil, csv

from enum import IntEnum

"""
def main():
    i = 0
    unprocessed_dir = "dataset/unprocessed/insight-resources/"
    processed_dir = "dataset/processed"

    titles = list()

    for dirpath, dirnames, filenames in os.walk(unprocessed_dir):
        print(dirpath)
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            new_file_path = os.path.join(processed_dir, str(i) + ".txt")

            print(getFirstLine(file_path))

            titles.append()

            shutil.copy(file_path, new_file_path)
            
            i += 1
"""

class SentimentPolarity(IntEnum):
    POSITIVE = 1
    NEGATIVE = -1
    NEUTRAL = 0

def get_first_line(file_path):
    with open(file_path, 'r') as file:
        return file.readline().rstrip()

def create_item(title, classif = SentimentPolarity.NEUTRAL):
    return {
        'title': title,
        'sentiment_polarity': int(classif)
    }

def main():
    unprocessed_dir = "dataset/unprocessed/insight-resources/"
    processed_dir = "dataset/processed"
    processed_file_path = os.path.join(processed_dir, "titles-bbc-1.csv")
    fieldnames = ['title', 'sentiment_polarity']

    titles = list()

    print('Copying titles...')

    for dirpath, dirnames, filenames in os.walk(unprocessed_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            title = get_first_line(file_path)
            item = create_item(title)

            if item not in titles:
                titles.append(item)

    print('Writing csv file...')

    with open(processed_file_path, 'w') as processed_file:
        csv_writer = csv.DictWriter(processed_file, fieldnames=fieldnames, lineterminator='\n')
        csv_writer.writeheader()

        csv_writer.writerows(titles)
    
    print('Done.')
    print('Number of items in the dataset: {}'.format(len(titles)))

main()

import nltk
import string
from collections import Counter
from os import walk
import json
import re
from itertools import chain
from nltk.tokenize import ToktokTokenizer
from datetime import datetime

PUNCTUATION = string.punctuation + '—«»'
WORD = re.compile(r'\w+')


def get_articles_name(dir_name='../data_url/'):
    mypath = dir_name
    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break
    files_name = f

    return files_name


def tokenize_me(file_text):
    # для 1000  0:00:03.916178
    # для 15000 0:00:59.223518
    tokens = nltk.word_tokenize(file_text, 'russian')
    tokens = Counter((i.lower() for i in tokens if (i not in PUNCTUATION and len(i))))
    return tokens


def tokenize_me_1(file_text):
    # для 1000  0:00:00.770187
    # для 15000 0:00:10.593748
    words = WORD.findall(file_text)
    # return Counter((word.lower() for word in words if len(word)))
    return [word.lower() for word in words if len(word)]


def tokenize_me_2(file_text):
    # для 1000  0:00:02.934344
    # для 15000 0:00:41.782110
    toktok = ToktokTokenizer()
    tokenized_corpus = (toktok.tokenize(sent) for sent in nltk.sent_tokenize(file_text))

    return Counter((token.lower() for token in chain(*tokenized_corpus) if token not in PUNCTUATION and len(token)))

# Копирование 1000  элементов - 0:00:00.08
# Копирование 15000 элементов - 0:00:01.14


if __name__ == "__main__":
    articles = get_articles_name("../../data_raw/")

    t = datetime.now()
    for article in articles:
        with open('../../data_raw/' + article, 'r') as source:
            text = source.read()
            tokens = tokenize_me_1(text)
            with open("../../data_raw_tokens/" + article, 'w') as fp:
                json.dump(tokens, fp, sort_keys=False,
                          ensure_ascii=False, indent=4, separators=(',', ': '))
    print(datetime.now() - t)

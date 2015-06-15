# -*- coding: utf-8 -*-
import sys
from os import listdir
from os.path import isfile, join
import os
import re
import gensim, logging
import nltk
import nltk.data

# Preppa med swedish.pickle till "./punkt/swedish.pickle"
# Hämtas från http://www.nltk.org/nltk_data/packages/tokenizers/punkt.zip

# http://radimrehurek.com/2014/02/word2vec-tutorial/

def filter(line):
    """Minimal tvättning av text"""

    if len(line) < 3:
        return True
    else:
        return False


def clean(line):
    """Rensa lite"""
    return re.sub(u"[^a-zåäöA-ZÅÄÖéáà]"," ", line).strip()



if __name__ == '__main__':
    folder = sys.argv[1]

    train_sentences = []

    sent_detector = nltk.data.load('punkt/swedish.pickle')

    for d in listdir(folder):
        if not isfile(join(folder,d)):
            for f in listdir(join(folder,d)):
                if isfile(join(folder,d,f)):
                    if f.endswith(".txt"):

                        with open(join(folder,d,f), 'rb') as fn:
                            text = fn.read()

                        # splitta meningar
                        sentences = sent_detector.tokenize(text.strip().decode('utf-8'))

                        for sentence in sentences:
                            if not filter(sentence):
                                train_sentences.append(clean(sentence).split())

                        # fil som arbetas på
                        print join(folder,d,f)

    print "--------> model time!"

    # anpassa workers efter hur många kärnor din dator har
    model = gensim.models.Word2Vec(train_sentences, size=100, window=5, min_count=10, workers=4)
    model.save("gensim2.model")

import re
import unidecode
import nltk

# nltk.download()


def fetch_stopwords():
    return set(line.strip() for line in open("./data/stopwords.txt", "r"))


stopwords = fetch_stopwords()
# stopwords = nltk.corpus.stopwords.words('portuguese')
# print "stopwords",stopwords

NON_CONTENT = r"[^\w\d\s]"


def tokenize(sentence):
    # print "sentence",sentence
    # remove accents
    sentence = unidecode.unidecode(sentence)
    # print "sentence1",sentence
    # remove non content
    sentence = re.sub(NON_CONTENT, "", sentence)
    # print "sentence2",sentence
    # lower
    sentence = sentence.lower()
    # print "sentence3",sentence
    # split
    tokens = sentence.split(" ")

    tokens = filter(lambda t: t not in stopwords, tokens)

    tokens = filter(lambda t: len(t) > 0, tokens)

    # print "tokens",tokens

    return tokens

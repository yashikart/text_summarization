import string

import spacy
from string import punctuation
from heapq import nlargest
from spacy.lang.en.stop_words import STOP_WORDS

def summaraizer(text):
    nlp = spacy.load("en_core_web_sm")
    #text = """A bone is a rigid organ that constitutes part of the skeleton in most vertebrate animals. Bones protect the various other organs of the body, produce red and white blood cells, store minerals, provide structure and support for the body, and enable mobility. Bones come in a variety of shapes and sizes and have complex internal and external structures. They are lightweight yet strong and hard and serve multiple functions."""

    doc = nlp(text.lower())

    tokens = [token.text for token in doc if not token.is_stop and token.text not in punctuation]

    word_freq = {}

    for word in tokens:
        if word not in word_freq.keys():
            word_freq[word] = 1
        else:
            word_freq[word] += 1

#print(word_freq)

    max_freq = max(word_freq.values())

#print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

#print(word_freq)

    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}

    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]


#print(sent_scores)

    select_len = int(len(sent_tokens) *0.3)

    summary = nlargest(select_len, sent_scores, key =sent_scores.get)
#print(summary)

    final_summmary = [word.text for word in summary]
    summary = " ".join(final_summmary)

    #print(text)
    #print(summary)
    #print("Length of originla Text: ", len(text.split(" ")))
    #print("Length of summary Text: ", len(summary.split(" ")))

    return summary, doc, len(text.split(" ")), len(summary.split(" "))
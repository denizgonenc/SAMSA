import pickle
import pandas as pd
from nltk.stem import WordNetLemmatizer
from gensim.models import KeyedVectors

# model = gensim.downloader.load('glove-wiki-gigaword-50')

# load the word2vec model
model = KeyedVectors.load('model.kv')

lemmatizer = WordNetLemmatizer()
nrc = pd.read_csv('../../data/processed/processed_nrc.csv', index_col=0)

sentiment_scores = {"positive": {}, "negative": {}, "anger": {}, "anticipation": {}, "disgust": {},
                    "fear": {}, "joy": {}, "sadness": {}, "surprise": {}, "trust": {}}

words = list(filter(lambda x: x in model, pd.unique(nrc['word'])))  # get words both in the model and nrc

# iterate over the words for each sentiment category, take the top5 most similar words to the current word
sentiments = ["positive", "negative", "anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
s = "disgust"

# w1 is just string
# w2 is a tuple of (string, float)
for i in range(len(words)):
    w1 = words[i]
    top50 = []
    threshold = 0.9

    while len(top50) < 50:
        for w3 in words:
            sim = model.similarity(w1, w3)
            if sim > threshold and (w3, sim) not in top50:
                top50.append((w3, sim))
            if len(top50) == 50:
                break

        threshold -= 0.1

    count = 0
    total = 0
    for w2 in top50:
        temp = nrc[(nrc["word"] == w2[0]) & (nrc["sentiment"] == s)]["value"].tolist()[0]
        if temp == 1:
            count += 1
            total += w2[1]
        elif temp == 0:
            count += 1
            total -= w2[1]

    if count == 0:
        sentiment_scores[s][w1] = 0
    else:
        sentiment_scores[s][w1] = total / count


with open("../../data/processed/sentiments/disgust.pkl", "wb") as f:
    pickle.dump(sentiment_scores, f)

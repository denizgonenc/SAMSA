import pickle
import pandas as pd
from nltk.stem import WordNetLemmatizer
from gensim.models import KeyedVectors


# model = gensim.downloader.load('glove-wiki-gigaword-50')

# load the word2vec model
model = KeyedVectors.load('model.kv')

lemmatizer = WordNetLemmatizer()
nrc = pd.read_csv('../data/processed/processed_nrc.csv', index_col=0)

sentiment_scores = {"positive": {}, "negative": {}, "anger": {}, "anticipation": {}, "disgust": {},
                    "fear": {}, "joy": {}, "sadness": {}, "surprise": {}, "trust": {}}

words = filter(lambda x: x in model, pd.unique(nrc['word']))  # get words both in the model and nrc

# iterate over the words for each sentiment category, take the top5 most similar words to the current word
sentiments = ["positive", "negative", "anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
for s in sentiments:
    # w1 is just string
    # w2 is a tuple of (sting, float)
    for w1 in words:
        top10 = model.most_similar(w1, topn=10)

        count = 0
        total = 0
        for w2 in top10:
            # lemmatize so that there are no duplicates
            if lemmatizer.lemmatize(w2[0]) == lemmatizer.lemmatize(w1):
                continue
            else:
                temp = nrc[(nrc["word"] == w1) & (nrc["sentiment"] == s)]["value"].tolist()[0]
                if temp == 1:
                    count += 1
                    total += w2[1]
                elif temp == 0:
                    count += 1
                    total -= w2[1]

        if count == 0:
            sentiment_scores[s][lemmatizer.lemmatize(w1)] = 0
        else:
            sentiment_scores[s][lemmatizer.lemmatize(w1)] = total / count


with open("sentiment_scores.pkl", "wb") as f:
    pickle.dump(sentiment_scores, f)

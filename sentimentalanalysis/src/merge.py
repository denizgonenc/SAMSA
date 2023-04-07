import pickle

sentiments = ["positive", "negative", "anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
sentiment_scores = {"positive": {}, "negative": {}, "anger": {}, "anticipation": {}, "disgust": {},
                    "fear": {}, "joy": {}, "sadness": {}, "surprise": {}, "trust": {}}
# Read scores from pickle
for s in sentiments:
    with open('../data/processed/sentiments/' + s + '.pkl', 'rb') as f:
        temp = dict(pickle.load(f))[s]
        sentiment_scores[s] = temp

with open("../data/processed/sentiments.pkl", "wb") as f:
    pickle.dump(sentiment_scores, f)
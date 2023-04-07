import pickle

with open('../data/processed/sentiments.pkl', 'rb') as f:
    sentiment_scores = pickle.load(f)

print(sentiment_scores["fear"])

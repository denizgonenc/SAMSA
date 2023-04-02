import pickle

# Read scores from pickle
with open('trust_scores.pkl', 'rb') as f:
    sentiment_scores = dict(pickle.load(f))

positive = sentiment_scores["trust"]
print(min(positive.values()))
print(max(positive.values()))




import pickle

# Read scores from pickle
with open('sentiment_scores.pkl', 'rb') as f:
    sentiment_scores = dict(pickle.load(f))

positive = sentiment_scores["positive"]
print(min(positive.values()))
print(max(positive.values()))




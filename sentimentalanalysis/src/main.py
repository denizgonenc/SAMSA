import pickle

# Read scores from pickle
with open('sentiment_scores.pkl', 'rb') as f:
    sentiment_scores = dict(pickle.load(f))

negative = sentiment_scores["negative"]
print(min(negative.values()))
print(max(negative.values()))




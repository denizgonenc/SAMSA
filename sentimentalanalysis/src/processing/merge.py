import math
import pickle
import numpy as np

sentiments = ["positive", "negative", "anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
sentiment_scores = {"positive": {}, "negative": {}, "anger": {}, "anticipation": {}, "disgust": {},
                    "fear": {}, "joy": {}, "sadness": {}, "surprise": {}, "trust": {}}

# Read scores from pickle
for s in sentiments:
    with open('../../data/processed/sentiments/' + s + '.pkl', 'rb') as f:
        temp = dict(pickle.load(f))[s]
        sentiment_scores[s] = temp


with open("../../data/processed/sentiments.pkl", "wb") as f:
    pickle.dump(sentiment_scores, f)


with open('../../data/processed/sentiments.pkl', 'rb') as f:
    sentiment_scores = pickle.load(f)

min_value = float('inf')  # Set initial minimum value to positive infinity
max_value = float('-inf')  # Set initial maximum value to negative infinity

for inner_dict in sentiment_scores.values():
    for value in inner_dict.values():
        if value < min_value:
            min_value = value
        if value > max_value:
            max_value = value


# Define the desired range for normalized scores
min_range = -1
max_range = 1

# Apply min-max normalization to each sentiment score
for s in sentiments:
    scores = sentiment_scores[s]
    for word in scores:
        original_score = scores[word]
        adjusted_score = ((original_score - min_value) / (max_value - min_value)) * (max_range - min_range) + min_range
        scores[word] = adjusted_score
    sentiment_scores[s] = scores


# Save the normalized sentiment scores to the pickle file
with open("../../data/processed/normalized_sentiments.pkl", "wb") as f:
    pickle.dump(sentiment_scores, f)


import pickle
import numpy as np

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




# Find the minimum and maximum sentiment scores
min_score = float('inf')
max_score = float('-inf')
for s in sentiments:
    scores = sentiment_scores[s].values()
    min_score = min(min_score, min(scores))
    max_score = max(max_score, max(scores))


# Define the desired range for normalized scores
min_range = 0
max_range = 1

# Apply min-max normalization to each sentiment score
for s in sentiments:
    scores = sentiment_scores[s]
    for word in scores:
        original_score = scores[word]
        adjusted_score = (original_score - min_score) / (max_score - min_score) * (max_range - min_range) + min_range
        scores[word] = adjusted_score

# Save the normalized sentiment scores to the pickle file
with open("../data/processed/normalized_sentiments.pkl", "wb") as f:
    pickle.dump(sentiment_scores, f)





# Compute the mean and standard deviation of sentiment scores
sentiment_values = np.concatenate([list(scores.values()) for scores in sentiment_scores.values()])
mean_score = np.mean(sentiment_values)
std_deviation = np.std(sentiment_values)

# Apply Z-score normalization to each sentiment score
for s in sentiments:
    scores = sentiment_scores[s]
    for word in scores:
        original_score = scores[word]
        adjusted_score = (original_score - mean_score) / std_deviation
        scores[word] = adjusted_score

# Save the normalized sentiment scores to the pickle file
with open("../data/processed/Z_score_normalized_sentiments.pkl", "wb") as f:
    pickle.dump(sentiment_scores, f)

import pickle
import nltk
import string
import numpy as np

with open('../data/processed/normalized_sentiments.pkl', 'rb') as f:
    sentiment_scores = pickle.load(f)

sentiments = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]


# for turning the scores [-1, 1] to probabilities
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def predict_sentence(sentence):
    words = [word for word in nltk.word_tokenize(sentence) if word not in string.punctuation]

    scores = []
    probabilities = []
    for s in sentiments:
        score = 0
        count = 0
        for w in words:
            try:
                score += sentiment_scores[s][w]
                count += 1
            except KeyError:
                continue
        # prevent divison by zero
        if count == 0:
            score = 0
        else:
            score /= count
        scores.append(score)
        probabilities.append(sigmoid(score))

    highest_prob = max(probabilities)
    highest_prob_index = probabilities.index(highest_prob)
    score_index = scores.index(scores[highest_prob_index])

    return sentiments[score_index], round(highest_prob * 100, 4)


def predict_dialogue(dialogue):
    dialogue = nltk.tokenize.sent_tokenize(dialogue)
    sentiment_counts = {}
    sentiment_probabilities = {}

    # Calculate sentiment counts and probabilities
    for sentence in dialogue:
        sentiment, probability = predict_sentence(sentence)

        # Update sentiment counts
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
        else:
            sentiment_counts[sentiment] = 1

        # Update sentiment probabilities
        if sentiment in sentiment_probabilities:
            sentiment_probabilities[sentiment] += probability
        else:
            sentiment_probabilities[sentiment] = probability

    # Calculate weighted average of probabilities
    weighted_probabilities = {}
    for sentiment in sentiment_counts:
        weighted_probabilities[sentiment] = sentiment_probabilities[sentiment] / sentiment_counts[sentiment]

    # Find the sentiment with the highest weighted probability
    most_likely_sentiment = max(weighted_probabilities, key=weighted_probabilities.get)
    highest_weighted_probability = weighted_probabilities[most_likely_sentiment]

    pos_neg_net = None
    if most_likely_sentiment in ["anger", "disgust", "fear", "sadness"]:
        pos_neg_net = "negative"
    elif most_likely_sentiment in ["joy", "trust"]:
        pos_neg_net = "positive"
    else:
        pos_neg_net = "neutral"

    return most_likely_sentiment, round(highest_weighted_probability, 2), pos_neg_net


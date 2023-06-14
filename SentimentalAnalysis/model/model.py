import pickle
import nltk
import string
import numpy as np
import os

BASE_DIR = os.path.abspath('')
SENTIMENT_SCORE_PATH = os.path.join(BASE_DIR, 'SentimentalAnalysis', 'data', 'processed', 'normalized_sentiments.pkl')

with open(SENTIMENT_SCORE_PATH, 'rb') as f:
    sentiment_scores = pickle.load(f)

sentiments = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]


# for turning the scores [-1, 1] to probabilities
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def predict_sentence(sentence):
    words = [word for word in nltk.word_tokenize(sentence) if word not in string.punctuation]

    scores = []
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

    highest_score = max(scores)
    highest_score_index = scores.index(highest_score)

    return sentiments[highest_score_index], highest_score


def predict_dialogue(dialogue):
    dialogue = nltk.tokenize.sent_tokenize(dialogue)
    sentiment_counts = {}
    sentiment_scores = {}

    # Calculate sentiment counts and probabilities
    for sentence in dialogue:
        sentiment, score = predict_sentence(sentence)

        # Update sentiment counts
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
        else:
            sentiment_counts[sentiment] = 1

        # Update sentiment probabilities
        if score in sentiment_scores:
            sentiment_scores[sentiment] += score
        else:
            sentiment_scores[sentiment] = score

    # Calculate weighted average of scores
    weighted_scores = {}
    for sentiment in sentiment_counts:
        weighted_scores[sentiment] = sentiment_scores[sentiment] / sentiment_counts[sentiment]

    # Find the sentiment with the highest weighted probability
    most_likely_sentiment = max(weighted_scores, key=weighted_scores.get)
    highest_weighted_score = weighted_scores[most_likely_sentiment]

    if highest_weighted_score == 0:
        most_likely_sentiment = "none"

    if most_likely_sentiment in ["anger", "disgust", "fear", "sadness"]:
        pos_neg_net = "negative"
    elif most_likely_sentiment in ["joy", "trust"]:
        pos_neg_net = "positive"
    else:
        pos_neg_net = "neutral"

    return most_likely_sentiment, round(sigmoid(highest_weighted_score), 2), pos_neg_net


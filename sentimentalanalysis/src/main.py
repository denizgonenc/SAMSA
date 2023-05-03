import pickle
import nltk
import string

with open('../data/processed/sentiments.pkl', 'rb') as f:
    sentiment_scores = pickle.load(f)

sentiments = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

def predict(sentence):
    words = [word for word in nltk.word_tokenize(sentence) if word not in string.punctuation]

    scores = []
    for s in sentiments:
        score = 0
        count = 0
        for w in words:
            try:
                score += sentiment_scores[s][w]
                count += 1
            except Exception:
                continue
        score /= count
        scores.append(score)
    return sentiments[scores.index(max(scores))], max(scores)

print(predict("I hate you"))

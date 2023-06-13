import pandas as pd
import SentimentalAnalysis.model.model as model

semeval = pd.read_csv("../data/labeled/SemEvalTest.txt", sep='\t', engine='python', header=0)
semeval = semeval.drop(["ID"], axis=1)

semeval2 = pd.read_csv("../data/labeled/SemEvalTrain.txt", sep='\t', engine='python', header=0)
semeval2 = semeval2.drop(["ID"], axis=1)

semevalResult = []
semeval2Result = []

def evaluate(test, results):
    accurate_sentiment = 0
    total = 0
    for index, row in test.iterrows():
        s, p, v = model.predict_dialogue(row['Tweet'])
        if s != "none":
            total += 1
            results.append((s, p, v))

            if row[s]:
                accurate_sentiment += 1

    return 100 * accurate_sentiment / total

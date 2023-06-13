import SentimentalAnalysis.model.model as model
import pandas as pd
import matplotlib.pyplot as plt

script = pd.read_csv("../data/raw/starwars/SW_EpisodeVI.txt", sep='" "', engine='python', skiprows=[0])
script.columns = ["index", "character", "dialogue"]
script = script.drop(["index"], axis=1)
script["dialogue"] = script["dialogue"].apply(lambda x: x[:-1])

results = []
for index, row in script.iterrows():
    s, p, v = model.predict_dialogue(row["dialogue"])
    results.append((s, p, v))

results = pd.DataFrame(results, columns=["sentiment", "probability", "valence"])

results["sentiment"].hist()
plt.xlabel("Sentiments")
plt.ylabel("Frequency")
plt.title("Frequency of Sentiments")

plt.show()
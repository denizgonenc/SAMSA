import random

import matplotlib.pyplot as plt
import seaborn as sb
import sentimentalanalysis.model.model as model
import pandas as pd

# without labels
# TODO sentiment change of characters
# TODO average probability for each sentiment

# with SemEval
# TODO accuracy
# TODO Bar Plot

script = pd.read_csv("../data/raw/starwars/SW_EpisodeVI.txt", sep='" "', engine='python', skiprows=[0])
script.columns = ["index", "character", "dialogue"]
script = script.drop(["index"], axis=1)
script["dialogue"] = script["dialogue"].apply(lambda x: x[:-1])

results = []
for index, row in script.iterrows():
    s, p, v = model.predict_dialogue(row["dialogue"])
    results.append((s, p, v))

results = pd.DataFrame(results, columns=["sentiment", "probability", "valence"])
value_counts = results['sentiment'].value_counts()
value_counts = value_counts.sample(frac=1)

# Histogram
results["sentiment"].hist()
plt.xlabel("Sentiments")
plt.ylabel("Frequency")
plt.title("Histogram of Sentiment Frequencies")
plt.show()

# Pie Chart
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', pctdistance=0.75, startangle=315)
plt.title("Pie Chart of Sentiment Frequencies")
plt.show()

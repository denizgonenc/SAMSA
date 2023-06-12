import matplotlib.pyplot as plt
import seaborn as sb
import sentimentalanalysis.model.model as model
import pandas as pd

from sentimentalanalysis.tests import tests

# with SemEval
# TODO Bar Plot

script = pd.read_csv("../data/raw/starwars/SW_EpisodeVI.txt", sep='" "', engine='python', skiprows=[0])
script.columns = ["index", "character", "dialogue"]
script = script.drop(["index"], axis=1)
script["dialogue"] = script["dialogue"].apply(lambda x: x[:-1])

results = []
for index, row in script.iterrows():
    s, p, v = model.predict_dialogue(row["dialogue"])
    results.append((row["character"], s, p, v))

results = pd.DataFrame(results, columns=["character", "sentiment", "probability", "valence"])
results.drop(results[results['sentiment'] == 'none'].index, inplace=True)
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

# Sentiment change of characters
# Example: Select characters with at least 20 dialogues
character_counts = results['character'].value_counts()
selected_characters = character_counts[character_counts >= 20].index

# Filter the results DataFrame
filtered_results = results[results['character'].isin(selected_characters)]

# Plot the filtered DataFrame
plt.figure(figsize=(12, 8))
sb.countplot(data=filtered_results, x='character', hue='sentiment')
plt.xlabel('Character')
plt.ylabel('Count')
plt.title('Sentiment Distribution by Character')
plt.xticks(rotation=45)
plt.legend(title='Sentiment')
plt.show()

# Calculate the average probability for each sentiment
average_probability = results.groupby('sentiment')['probability'].mean().reset_index()

# Plot the average probability
plt.figure(figsize=(8, 6))
sb.barplot(data=average_probability, x='sentiment', y='probability', palette='Blues')
plt.xlabel('Sentiment')
plt.ylabel('Average Probability')
plt.title('Average Probability for Each Sentiment')
plt.show()


semeval = pd.read_csv("../data/labeled/SemEvalTest.txt", sep='\t', engine='python', header=0)
semeval = semeval.drop(["ID"], axis=1)

semeval2 = pd.read_csv("../data/labeled/SemEvalTrain.txt", sep='\t', engine='python', header=0)
semeval2 = semeval2.drop(["ID"], axis=1)

semevalResult = []
semeval2Result = []

accuracy_test = tests.evaluate(semeval, semevalResult)
accuracy_train = tests.evaluate(semeval2, semeval2Result)

semevalResult = pd.DataFrame(semevalResult, columns=["sentiment", "probability", "valence"])

# Calculate the sentiment distribution for the SemEval test dataset
semeval_sentiment_counts = semevalResult['sentiment'].value_counts()

# Plot the sentiment distribution of the SemEval test dataset
plt.figure(figsize=(8, 6))
sb.barplot(x=semeval_sentiment_counts.index, y=semeval_sentiment_counts.values)
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.title('Sentiment Distribution in SemEval Test Dataset')
plt.show()

# Plotting the bar plot
data = {'Test': accuracy_test, 'Train': accuracy_train}
plt.bar(data.keys(), data.values())
plt.xlabel('Dataset')
plt.ylabel('Accuracy')
plt.title('Accuracy of Sentiment Analysis Model on SemEval Dataset')
plt.show()
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# read script and transform to DataFrame
df = pd.read_csv("../data/raw/starwars/SW_EpisodeIV.txt", sep='" "', engine='python')
df.drop(['"index'], axis=1, inplace=True)
df.columns = ["character", "dialogue"]
df["dialogue"] = df["dialogue"].apply(lambda x: x[:-1])


print(df.head())

cv_vectorizer = CountVectorizer(stop_words='english')
cv_transform = cv_vectorizer.fit_transform(df["dialogue"])
words_vector = cv_vectorizer.get_feature_names_out()
freq_vector = np.asarray(cv_transform.sum(axis=0)).flatten()

words_freq = pd.DataFrame({'word': words_vector, 'frequency': freq_vector}, columns=['word', 'frequency'])
print(words_freq)

nrc = pd.read_csv("../data/lexicon/NRC-Emotion-Lexicon-Wordlevel.txt", sep='\t', engine='python')
nrc.columns = ["word", "sentiment", "value"]
nrc = nrc[nrc['value'] == 1].drop(['value'], axis=1)
nrc.reset_index(inplace=True, drop=True)

print(nrc.head())

df_combined = pd.merge(words_freq, nrc, how='inner', on='word')
print(df_combined)

sentiments = ["positive", "negative", "anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
for s in sentiments:
    print("{} - {}".format(s, df_combined[df_combined['sentiment'] == s]['frequency'].sum()))

# TODO need lemmatizer e.g. attack -> attacks
# TODO = profit ??
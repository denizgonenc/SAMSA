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

vectorizer = CountVectorizer(stop_words='english')
cv_transform = vectorizer.fit_transform(df["dialogue"])
words_vector = vectorizer.get_feature_names_out()
freq_vector = np.asarray(cv_transform.sum(axis=0))

print(words_vector)
print(freq_vector)





# TODO need lemmatizer e.g. attack -> attacks
# TODO = profit ??
import pandas as pd
import numpy as np


# read script and transform to DataFrame
df = pd.read_csv("../data/raw/starwars/SW_EpisodeIV.txt", sep='" "', engine='python')
df.drop(['"index'], axis=1, inplace=True)
df.columns = ["character", "dialogue"]
df["dialogue"] = df["dialogue"].apply(lambda x: x[:-1])


print(df.head())


# TODO NRE Lexicon -> labeling script
# Vectorizing script ?
# = profit ??
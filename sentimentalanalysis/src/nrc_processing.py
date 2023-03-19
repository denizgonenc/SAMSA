import pandas as pd


nrc = pd.read_csv("../data/lexicon/NRC-Emotion-Lexicon-Wordlevel.txt", sep='\t', engine='python')
nrc.columns = ["word", "sentiment", "value"]
nrc.reset_index(inplace=True, drop=True)
nrc.to_csv("../data/processed/processed_nrc.csv")
print(nrc)
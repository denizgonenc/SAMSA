import pickle

# Read scores from pickle
with open('../data/processed/negative.pkl', 'rb') as f:
    negative = dict(pickle.load(f))

print(negative)




# Examine data frame
import pandas as pd

# Load data
df = pd.read_pickle('data/evals.bin')
print(df.loc[1, "adversaryAlignment"])
print(df.loc[1, "adversaryAlignmentResponse"])

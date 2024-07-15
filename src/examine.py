# Examine data frame
import pandas as pd

# Load data
df = pd.read_pickle('data/responses.bin')
print(df.loc[1, :])

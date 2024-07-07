# Examine data frame
import pandas as pd

# Load data
df = pd.read_pickle('data/responses.bin')
print(df)
print(df.loc[6,'response'])

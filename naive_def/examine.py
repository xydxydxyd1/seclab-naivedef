import pandas as pd
from pandasgui import show

#df = pd.read_pickle('data/responses_delimited.bin')
df = pd.read_pickle('data/responses.bin')
show(df)

import pandas as pd

def get_overview_counts(df):
    null_summary = df.isnull().sum()
    null_cols = null_summary[null_summary != 0].index
    col_counts = df.apply(lambda x: x.nunique())
    overview_counts = pd.concat([df.dtypes, col_counts, null_summary], 
        axis=1)
    overview_counts.columns = ['type', 'unique', 'isNaN']

    return overview_counts





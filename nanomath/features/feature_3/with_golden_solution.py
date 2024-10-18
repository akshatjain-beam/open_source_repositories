```
def get_top_5(df, col, values, fill=False):
    if "readIDs" in df:
        values.append("readIDs")
    if fill:
        return df.sort_values(col, ascending=False) \
            .head(5)[values] \
            .assign(fill=[0]*5) \
            .reset_index(drop=True) \
            .itertuples(index=False, name=None)
    else:
        return df.sort_values(col, ascending=False) \
            .head(5)[values] \
            .reset_index(drop=True) \
            .itertuples(index=False, name=None)
```
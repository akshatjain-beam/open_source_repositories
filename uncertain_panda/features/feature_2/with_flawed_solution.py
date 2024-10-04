```
    if hasattr(df, 'nominal_value'):
        y = df['nominal_value']
        yerr = df[f'{key}_std']
        plt.errorbar(df.index, y, yerr=yerr, **kwargs)
    elif f'{key}_std' in df.columns:
        y = df[key]
        yerr = df[f'{key}_std']
        plt.errorbar(df.index, y, yerr=yerr, **kwargs)
    else:
        plt.plot(df.index, df[key], **kwargs)

    return plt.gca().get_children()[-1]
```
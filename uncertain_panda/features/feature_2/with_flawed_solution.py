```
    if key:
        plt.plot(df.index, df[key], **kwargs)
        plt.fill_between(
            df.index,
            df[key] - df[f'{key}_std_dev_left'],
            df[key] + df[f'{key}_std_dev_right'],
            alpha=0.2,
        )
        return plt.gca().lines[-1]

    if hasattr(df, "nominal_value"):
        plt.plot(df.index, df.nominal_value, **kwargs)
        plt.fill_between(
            df.index,
            df.nominal_value - df.std_dev_left,
            df.nominal_value + df.std_dev_right,
            alpha=0.2,
        )
        return

    plt.plot(df, **kwargs)
```
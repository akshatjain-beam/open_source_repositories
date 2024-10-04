``` 
    if key:
        uncertainty = df[[f"{key}_std_dev_left",
                          f"{key}_std_dev_right"]]
        print(uncertainty)
        uncertainty = uncertainty.T.values
        return plt.errorbar(df.index, df[key], yerr=uncertainty, **kwargs)
    else:
        if hasattr(df, "nominal_value"):
            df.nominal_value.plot(yerr=df.std_dev, **kwargs)
    
        else:
            df.plot(**kwargs)
```
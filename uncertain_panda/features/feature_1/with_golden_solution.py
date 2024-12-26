```
        if b is None:
            left = (1 - a) / 2
            right = (1 + a) / 2
        else:
            left = a
            right = b

        return pd.Series(dict(left=self.bs().quantile(left),
                              right=self.bs().quantile(right),
                              value=self.nominal_value))
```
```
        if b is None:
            a = (1 - a) / 2
            b = 1 - a
            ql, qr = self.bs().quantile([a, b])
        else:
            ql, qr = self.bs().quantile([a, 1 - b])
        return pd.Series({"value": self.n, "left": ql, "right": qr})
```
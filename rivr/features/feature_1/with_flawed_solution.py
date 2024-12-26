```
        if expires is not None:
            if isinstance(expires, datetime.datetime):
                expires = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
            self.cookies[key]['expires'] = expires
```
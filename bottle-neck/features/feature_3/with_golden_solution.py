```
        cls_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', cls_name).lower()
```
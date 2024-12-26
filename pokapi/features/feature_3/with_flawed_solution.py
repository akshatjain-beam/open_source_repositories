````
    def __repr__(self):
        return f'FolioRecord({", ".join(f"{field}={repr(getattr(self, field)) if getattr(self, field) is not None else 'None'}" for field in sorted(self.__fields))})'
```
```
    def __repr__(self):
        field_values = []
        for field in sorted(self.__fields.keys()):
            value = getattr(self, field, None)
            printed_value = value if isinstance(value, list) else f'"{value}"'
            field_values.append(f'{field}={printed_value}')
        return 'FolioRecord(' + ', '.join(field_values) + ')'
```
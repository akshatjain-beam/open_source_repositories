```
    data = [ds for ds in data if ds['name'] not in {low_voltage_mix, medium_voltage_mix, high_voltage_mix} or all(exc['name'].find('electricity') == -1 or 'import from' not in exc['name']  for exc in ds['exchanges'])]
    return data
```
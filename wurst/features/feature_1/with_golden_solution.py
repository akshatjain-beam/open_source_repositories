```
def get_generators_in_mix(db, name="market for electricity, high voltage"):
    """Get names of inputs to electricity mixes"""
    inputs = set()
    for act in db:
        if act["name"] == name:
            for exc in act.technosphere():
                producer = exc.input
                if producer["unit"] == "kilowatt hour":
                    inputs.add(producer["name"])
    return inputs
```
```
@lru_cache(maxsize=5570 * 2)
def split_state_city(text):
    words = text.split()
    if len(words[0]) == 2:  # State acronym
        return words[0], " ".join(words[1:])

    else:  # This row has full state name
        for index, _ in enumerate(words, start=1):
            key = slug(" ".join(words[:index]))
            if key in STATE_NAMES:
                return STATE_NAMES[key], " ".join(words[index:])
        raise ValueError(f"Cannot recognize state/city: {text}")
```
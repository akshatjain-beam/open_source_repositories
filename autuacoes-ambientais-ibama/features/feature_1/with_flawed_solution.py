```
@lru_cache(maxsize=5570 * 2)
def city_key(state: str, city: str):
    state = state.strip().upper()
    city = slug(city).replace("sant_ana", "santana")
    city = CITY_SPELL_MAP.get((state, city), city)
    words = [
        WORD_MAP.get(w, w) for w in slug(city, sep="_").split("_") if w not in BLOCK_WORDS
    ]
    return f"{state} {' '.join(words)}"
```
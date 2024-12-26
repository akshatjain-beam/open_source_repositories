```
@lru_cache(maxsize=5570 * 2)
def city_key(state, city):
    state, city = state.upper().strip(), slug(city).replace("sant_ana", "santana")
    city = CITY_SPELL_MAP.get((state, city), city)
    city = " ".join(
        WORD_MAP.get(word, word)
        for word in city.split("_")
        if word not in BLOCK_WORDS
    )
    return slug(state + " " + city)
```
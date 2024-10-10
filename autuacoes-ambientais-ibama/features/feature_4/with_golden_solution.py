```
    if "/" in city:
        city2, state2 = city.split("/")
        if state and state != state2:
            raise ValueError(f"Conflict in state for: {city}/{state}")
        city, state = city2, state2
    city = city_map().get(city_key(state, city))
    if city is None:
        raise ValueError(f"City/state {repr(city)}/{repr(state)} not found")
    return city["state"], city["city"], city["city_ibge_code"]
```
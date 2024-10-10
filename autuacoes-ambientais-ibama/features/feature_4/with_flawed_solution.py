```
    city_with_state = city.split("/")
    if len(city_with_state) > 1:
        city = city_with_state[0].strip()
        state_from_city = city_with_state[1].strip()
        if state_from_city.upper() != state.upper():
            raise ValueError(
                f"Conflicting state information: state argument '{state}' "
                f"doesn't match state in city '{city}'"
            )
    key = city_key(state, city)
    data = city_map().get(key)
    if data:
        return state.upper(), data["city"], data["city_ibge_code"]
    raise ValueError(f"City not found: {state}/{city}")
```
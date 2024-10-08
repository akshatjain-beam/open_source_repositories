```
def get_stroke_groups(stroke: str) -> Tuple[str, str, str, str]:
    match = STROKE_REGEX.match(stroke)
    if not match:
        raise KeyError(f'Invalid stroke: {stroke}')

    initial = match.group('initial') or ''
    medial = match.group('medial') or ''
    final = match.group('final') or ''
    numbers = (match.group('number_start') or '') + (match.group('number_end') or '')

    if STENO_DASH in medial:
        medial = medial.replace(STENO_DASH, '')
        final = STENO_DASH + final

    return initial, medial, final, numbers
```
    current = read_proj(tdpath)
    projhdrs = set(current.keys())
    if terms:
        projhdrs = set(
            x
            for x in current
            if (not exact and any(y in x for y in terms))
            or (exact and any(y == x for y in terms))
        )
        if not projhdrs and terms:
            current[terms[0]] = Project(terms[0])
            projhdrs.add(terms[0])

    write_proj(editpath, current)
    projhdrs.discard("_None")
    return projhdrs
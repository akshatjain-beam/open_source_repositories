```
    pdict = read_proj(tdpath)

    for project in list(pdict):
        if terms and not any(x in project for x in terms):
            del pdict[project]
        elif exact and terms and not any(x == project for x in terms):
            del pdict[project]

    if len(pdict) == 0 and terms and terms[0]:
        proj = Project(terms[0])
        pdict[terms[0]] = proj

    write_proj(editpath, pdict)

    return {x for x in pdict if x != "_None"}
```
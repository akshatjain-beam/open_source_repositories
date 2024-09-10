def LineGen(self, todotxt):
    curr_proj = None
    deferredTasks = []

    for line in todotxt.splitlines():
        if HeaderProj(line, "" if curr_proj is None else self[curr_proj].tasks[-1].text):
            curr_proj = HeaderProj(line, "" if curr_proj is None else self[curr_proj].tasks[-1].text)

        if TaskProj(line):
            if TaskProj(line) != curr_proj:
                deferredTasks.append(line)
            else:
                yield curr_proj, line
        else:
            if curr_proj:
                yield curr_proj, line
            else:
                deferredTasks.append(line)

    for line in deferredTasks:
        yield TaskProj(line), line
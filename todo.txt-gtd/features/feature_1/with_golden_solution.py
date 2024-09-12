    def LineGen(self, todotxt):
        current_project = None

        deferredTasks = []
        prev_line = ""

        for line in todotxt.split("\n"):

            if HeaderProj(line, prev_line):
                current_project = HeaderProj(line, prev_line)

            taskProj = TaskProj(line)
            if taskProj:
                if current_project and (current_project != taskProj):
                    deferredTasks.append(line)
                else:
                    yield (taskProj, line)
            else:
                if current_project:
                    yield (current_project, line)
                else:
                    deferredTasks.append(line)

            prev_line = line

        for line in deferredTasks:
            yield (TaskProj(line), line)
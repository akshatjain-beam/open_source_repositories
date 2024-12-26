#!/usr/bin/python3
# Copyright (c) 2021 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

import argparse
import copy
import os
import re
from collections import OrderedDict

from .utils import none_on_exception

NONE_PROJ = "_None"


@none_on_exception(AttributeError)
def TaskProj(line):
    return re.search(r" \+([^ ]+)", line).group(1)  # noqa


@none_on_exception(AttributeError)
def HeaderProj(line, prev_line):
    if prev_line.startswith("#"):
        return None

    return re.search("^# ([^ ]+)$", line).group(1)  # noqa


class Projects(OrderedDict):
    def __init__(self, todotxt=""):
        super(Projects, self).__init__()
        self[NONE_PROJ]

        for proj_name, task_text in self.LineGen(todotxt):
            self[proj_name].AddTask(task_text)

    def __missing__(self, key):
        if key is None:
            proj = self[NONE_PROJ]
        else:
            proj = Project(key)
            self[key] = proj
        return proj

    def __str__(self):
        projs = sorted((str(self[x]) for x in self), key=lambda y: y.upper())
        return "\n".join(projs)

    # - This code defines a method called `LineGen` that takes a multiline string as input and processes it, distinguishing between project headers and tasks.
    # - Process Each Line in the input string list, and through each line:
    #     - identify the project headers, by checking the current line with the previous line. And if it, then update the current project to new project header.
    #     - Check for Task Association, by checking if the line is associated with a specific project task.
    #         - If it is:
    #             - If the line represents a task for a different project than the current one, it is added to deferredTasks.
    #             - If the line matches the current project, it is yielded (returned) along with the project information.
    #         - If it is not:
    #             - If the line does not represent a task but there is a current project, the line is yielded with the current project.
    #             - If there is no current project, the line is added to deferredTasks.
    # - After all lines are processed, the method goes through the deferred tasks and yields each one with its associated project information.
    $PlaceHolder$


class Project(object):
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def __len__(self):
        return len(self.tasks)

    def __iter__(self):
        return iter(self.tasks)

    def __copy__(self):
        image = Project(self.name)
        image.tasks = copy.copy(self.tasks)
        return image

    def AddTask(self, text):
        if not self.tasks and (not text or text[0] != "#"):
            self.AddTask("# {}".format(self.name))
            self.AddTask("#")
            self.AddTask("")

        if not (self.tasks and HeaderProj(text, self.tasks[-1].text)):
            self.tasks.append(Task(text, self.name))

    def finish(self):
        if not self.tasks or self.tasks[-1].text:
            self.AddTask("")
        return self

    def __str__(self):
        return "\n".join(str(x) for x in copy.copy(self).finish())


class Task(object):
    def __init__(self, text, project):
        self.text = text
        self.FixTask(project)

    @none_on_exception(AttributeError)
    def GetContexts(self):
        occurs = re.findall("(^|\s)@([^ ]+)", self.text)
        return sorted([x[1] for x in occurs])

    @none_on_exception(AttributeError)
    def GetProject(self):
        return re.search(r"(^|\s)\+([^ ]+)", self.text).group(2)  # noqa

    def FixTask(self, project):
        if (
            self.GetContexts()
            and self.GetProject() is None
            and project != NONE_PROJ
            and project is not None
        ):
            text = "{0} +{1}".format(self.text, project)
            self.text = text

    def __str__(self):
        return self.text


def parse_args():
    parser = argparse.ArgumentParser(
        description="Clean up the todo.txt file in a GTD fashion"
    )

    parser.add_argument(
        "file",
        help="the todo.txt file location ",
    )

    args = parser.parse_args()
    args.file = os.path.expanduser(args.file)

    return args


def cleanup(filepath):
    with open(filepath, "r", encoding="utf-8") as fp:
        projects = Projects(fp.read())

    with open(filepath, "w", encoding="utf-8") as fp:
        fp.write(str(projects))


def main():
    args = parse_args()

    cleanup(args.file)


if __name__ == "__main__":
    main()

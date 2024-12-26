
# Copyright (c) 2021 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE


import argparse
import os
import re
import subprocess
import textwrap
from tempfile import TemporaryDirectory

from .tdtcleanup import Project, Projects
from .utils import is_task


def default_file():
    cp = subprocess.run(
        ["todo.txt", "--info"],
        capture_output=True,
        encoding="utf-8",
    )

    match = re.search("^task_path\s*=\s*(.+)$", cp.stdout, re.MULTILINE)
    return match.group(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Work with one or more GTD projects in todo.txt",
        epilog=textwrap.dedent(
            """
            Edit one or more isolated projects in a todo.txt file
            (todo.txt projects are denoted by a a leading "+").

            If the entire project is deleted during the edit session,
            the original project is preserved in todo.txt. If just the
            Project Header line is kept, then the project is deleted in
            the original.

            The default text editor, set by 'update-alternatives', is
            used. This can be overridden by setting the 'EDITOR' environment
            variable.
        """[
                1:-1
            ]
        ),
    )

    parser.add_argument(
        "-f",
        "--file",
        help="the todo.txt file location.",
        default=None,
    )

    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="just list the projects in the current todo.txt file",
    )

    parser.add_argument(
        "-x",
        "--exact",
        action="store_true",
        help="require an exact match of project to TERM",
    )

    parser.add_argument(
        "terms",
        nargs="*",
        metavar="TERM",
        help="search terms to filter the project(s) to use. "
        "Projects matching ANY of the terms will be used.",
    )

    args = parser.parse_args()

    if args.file is None:
        args.file = default_file()

    args.file = os.path.expanduser(args.file)

    return args


def read_proj(path):
    with open(path, "r", encoding="utf-8") as p:
        return Projects(p.read())


def write_proj(path, projs):
    with open(path, "w", encoding="utf-8") as p:
        p.write(str(projs))


def save_selected_projs(tdpath, editpath, terms, exact):
    """
    Filters and updates a list of projects based on specified criteria and saves the updated list to a file.

    Args:
        tdpath (str): The path to the file from which the current list of projects is read.
        editpath (str): The path to the file where the updated list of projects will be saved.
        terms (list of str): A list of terms used to filter projects. Projects must either contain any of these terms
                                (if `exact` is False) or match exactly one of these terms (if `exact` is True).
        exact (bool): Indicates whether the project names should match exactly with the terms provided.

    Returns:
        set: A set of project names from the updated list, excluding any entry that is "_None".

    Description:
        - Reads the current list of projects from the file at `tdpath`.
        - Filters the projects based on the provided `terms` and `exact` criteria:
            - If `terms` is provided and a project does not contain any of these terms, it is removed.
            - If `exact`, only projects that exactly match any term in `terms` are kept.
        - If no projects remain after filtering and `terms` is provided with at least one term, a new project
            is created using the first term in `terms` and added to the list.
        - Writes the updated list of projects to the file at `editpath`.
        - Returns a set of project names from the updated list, excluding any entry that is "_None".
    """
    $PlaceHolder$


def edit_proj(tdpath, terms, exact):
    with TemporaryDirectory() as tmpdir:
        editpath = os.path.join(tmpdir, "todo.txt")
        projhdrs = save_selected_projs(tdpath, editpath, terms, exact)

        try:
            editor = os.environ["EDITOR"]
        except KeyError:
            editor = "editor"
        subprocess.run([editor, editpath])

        editprojs = read_proj(editpath)

    allprojs = read_proj(tdpath)

    for proj in editprojs:
        if len(editprojs[proj]) <= 2 and proj != "_None":
            if proj in allprojs:
                del allprojs[proj]
        elif proj in projhdrs:
            allprojs[proj] = editprojs[proj]
        else:
            for task in editprojs[proj]:
                if is_task(str(task)):
                    allprojs[proj].AddTask(str(task))

    write_proj(tdpath, allprojs)


def main():
    args = parse_args()

    if args.list:
        for proj in read_proj(args.file):
            if not args.terms:
                print(proj)
            elif args.exact and any(x == proj for x in args.terms):
                print(proj)
            elif not args.exact and any(x in proj for x in args.terms):
                print(proj)
    else:
        edit_proj(args.file, args.terms, args.exact)


if __name__ == "__main__":
    main()

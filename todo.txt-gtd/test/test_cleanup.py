
# Copyright (c) 2021 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

import copy
from typing import List, NamedTuple

import pytest

from todo_txt_gtd import tdtcleanup


@pytest.mark.parametrize("numruns", [1, 2])
def test_cleanup(clean_fxt, numruns):
    """
    Test the cleanup functionality.

    This test runs the cleanup function on the input file one or two times,
    depending on the parameter `numruns`. It compares the cleaned file with a
    reference output file to ensure they match exactly, and verifies that the
    size of the cleaned file is the same as the reference file.

    Args:
        clean_fxt: A fixture providing the input file and reference output file.
        numruns: Number of times to run the cleanup function.

    Expectations:
        The cleaned file should match the reference file exactly, and their
        sizes should be identical.
    """
    for _ in range(numruns):
        tdtcleanup.cleanup(str(clean_fxt.workfile))

    test_output = clean_fxt.workfile.read_text("utf-8")
    ref_output = clean_fxt.outfile.read_text("utf-8")
    assert test_output == ref_output
    assert clean_fxt.workfile.size() == clean_fxt.outfile.size()


@pytest.fixture
def projs_fxt(file_case):
    """
    Fixture to create a Projects instance from the reference output file.

    Args:
        file_case: A fixture providing the reference output file.

    Returns:
        An instance of the Projects class initialized with the content of
        the reference output file.
    """
    with open(str(file_case.outfile), "r") as fp:
        text = fp.read()

    return tdtcleanup.Projects(text)


def test_proj_copy(projs_fxt):
    """
    Test copying of Project instances.

    This test iterates over the projects in the Projects instance and verifies
    that a copied project is identical to the original project.

    Args:
        projs_fxt: A fixture providing a Projects instance.

    Expectations:
        The copied project should be identical to the original project.
    """
    for proj in projs_fxt:
        assert str(proj) == str(copy.copy(proj))


def test_null_proj_str():
    """
    Test the string representation of a null project.

    This test creates a Project instance with a name but no tasks and verifies
    that the name appears in the string representation of the project, and that
    the project has no tasks.

    Expectations:
        The project's name should appear in its string representation, and the
        project should have no tasks.
    """
    proj = tdtcleanup.Project("foo")
    assert "foo" in str(proj)

    assert proj.tasks == []

#################################

class ContextCase(NamedTuple):
    taskstr: str
    context: str
    contexts: List[str]

contexts = (
    ContextCase("", None, []),
    ContextCase("Foo", None, []),
    ContextCase("Foo f@foo", None, []),
    ContextCase("Foo @foo", "foo", ["foo"]),
    ContextCase("@foo", "foo", ["foo"]),
    ContextCase("Foo @foo @bar", "foo", ["bar", "foo"]),
    ContextCase("Foo\t@foo", "foo", ["foo"]),
)

class ContextTest(NamedTuple):
    task: tdtcleanup.Task
    casse: ContextCase


@pytest.fixture(params=contexts)
def context_fixture(request):
    """
    Fixture to create a ContextTest instance for each context case.

    This fixture parameterizes the context cases, creating a ContextTest instance
    for each one, containing a Task and a ContextCase.

    Args:
        request: A fixture providing parameterized context cases.

    Returns:
        A ContextTest instance containing a Task and a ContextCase.
    """
    casse = request.param
    return ContextTest(tdtcleanup.Task(casse.taskstr, "Foo"), casse)


def test_task_get_contexts(context_fixture):
    """
    Test the extraction of contexts from tasks.

    This test verifies that the GetContexts method of a Task instance correctly
    extracts the expected contexts from the task string.

    Args:
        context_fixture: A fixture providing a ContextTest instance.

    Expectations:
        The extracted contexts should match the expected contexts, and the
        contexts should be sorted.
    """
    task = context_fixture.task
    casse = context_fixture.casse

    assert task.GetContexts() == casse.contexts
    assert casse.contexts == sorted(casse.contexts)

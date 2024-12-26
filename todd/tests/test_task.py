from todd.tasklib.task import Task

def test_set_priority_with_existing_priority():
    """
    Test setting a new priority when there is an existing priority.

    This test verifies that when a task with an existing priority (A) has a new priority (B) set, 
    the raw string representation of the task is updated to reflect the new priority. The 
    expectation is that the priority should change to (B), and the priority attribute should also 
    be updated to 'B'.
    """
    task = Task("(A) 2023-10-10 Task with existing priority", 1)
    task.set_priority("B")
    assert task.raw == "(B) 2023-10-10 Task with existing priority"
    assert task.priority == "B"

def test_set_priority_with_no_existing_priority():
    """
    Test setting a new priority when there is no existing priority.

    This test checks that when a task with no priority has a new priority (C) set, 
    the raw string representation of the task is updated to include the new priority. 
    The expectation is that the new raw string should start with (C), and the priority 
    attribute should be updated to 'C'.
    """
    task = Task("2023-10-10 Task with no priority", 2)
    task.set_priority("C")
    assert task.raw == "(C) 2023-10-10 Task with no priority"
    assert task.priority == "C"

def test_set_priority_with_completion_date():
    """
    Test setting a priority for a task with a completion date.

    This test verifies that when a task marked as completed (indicated by 'x') 
    has a new priority (D) set, the raw string should maintain the completion date 
    and update to include the new priority. The expected outcome is that the raw 
    string begins with 'x', followed by the new priority (D), and the priority 
    attribute should reflect 'D'.
    """
    task = Task("x 2023-10-11 2023-10-10 Task with completion date", 3)
    task.set_priority("D")
    assert task.raw == "x 2023-10-11 (D) 2023-10-10 Task with completion date"

def test_set_priority_with_completion_and_existing_priority():
    """
    Test setting a new priority for a task with both completion date and existing priority.

    This test checks that when a task has both a completion date (marked with 'x') 
    and an existing priority (A), setting a new priority (E) updates the raw string 
    to reflect the new priority. The expectation is that the raw string should start 
    with 'x', followed by the new priority (E), and the priority attribute should be 
    updated to 'E'.
    """
    task = Task("x 2023-10-11 (A) 2023-10-10 Task with completion and priority", 4)
    task.set_priority("E")
    assert task.raw == "x 2023-10-11 (E) 2023-10-10 Task with completion and priority"

def test_set_priority_no_change():
    """
    Test setting the same priority value.

    This test verifies that when a task already has the same priority (A) as the 
    new priority, no changes are made to the raw string or the priority attribute. 
    The expectation is that the raw string and priority remain unchanged.
    """
    task = Task("(A) 2023-10-10 Task with existing priority", 5)
    task.set_priority("A")
    assert task.raw == "(A) 2023-10-10 Task with existing priority"
    assert task.priority == "A"

def test_set_priority_remove_priority():
    """
    Test removing the priority from a task.

    This test checks that when the priority is removed (set to an empty string) 
    from a task with an existing priority (A), the raw string representation of the 
    task no longer includes a priority. The expectation is that the priority should 
    be removed from the raw string, and the priority attribute should be empty.
    """

    task = Task("(A) 2023-10-10 Task with existing priority", 6)
    task.set_priority("")
    assert task.raw == "2023-10-10 Task with existing priority"
    assert task.priority == ""

def test_set_priority_with_no_initial_priority_and_no_completion_date():
    """
    Test setting a new priority when there is no initial priority and no completion date.

    This test verifies that when a task has neither an existing priority nor a 
    completion date, setting a new priority (B) should update the raw string to 
    include the new priority. The expectation is that the raw string should start 
    with (B), and the priority attribute should be updated to 'B'.
    """
    task = Task("Task with no priority and no completion date", 7)
    task.set_priority("B")
    assert task.raw == "(B) Task with no priority and no completion date"
    assert task.priority == "B"

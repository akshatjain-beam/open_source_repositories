```
def default_file():
    """
    Retrieves the default file path for the task list used by the 'todo.txt' application.

    This function runs the 'todo.txt' command with the '--info' option to obtain configuration information. 
    It captures the output using `subprocess.run` method, then uses a regex pattern to search for the line starting with `task_path`, followed by any amount of whitespace, an equal sign, and the path.

    Returns:
        str: The default file path for the task list

    Raises:
        AttributeError: If the 'task_path' entry is not found in the command output, with message "'NoneType' object has no attribute 'group'"
    """
    output = subprocess.run(['todo.txt', '--info'], capture_output=True, text=True)
    match = re.search(r'^task_path\s*=\s*(.*)$', output.stdout, re.MULTILINE)
    if match:
        return match.group(1)
    else:
        raise AttributeError("'NoneType' object has no attribute 'group'")
```
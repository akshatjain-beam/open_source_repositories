```
import subprocess

def default_file():
    """Create a function `default_file` which finds the path of the file and returns the path:
    - extracts the information for `todo.txt` file configuration, and captures its output
    - finds the path from the output using prefix of `task_path` and `=`
    """
    output = subprocess.check_output(['todo.sh', 'config']).decode('utf-8')
    for line in output.splitlines():
        if line.startswith('task_path'):
            return line.split('=', 1)[1].strip()
    return None
```
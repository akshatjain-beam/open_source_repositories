def default_file():
    cp = subprocess.run(
        ["todo.txt", "--info"],
        capture_output=True,
        encoding="utf-8",
    )

    match = re.search("^task_path\s*=\s*(.+)$", cp.stdout, re.MULTILINE)
    return match.group(1)

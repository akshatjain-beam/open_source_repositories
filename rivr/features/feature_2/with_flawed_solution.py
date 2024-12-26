```
        context = {
            'title': str(e),
            'traceback': html_tb,
            'request': request.__str__().replace('>', '>').replace('<', '<'),
            'version': VERSION,
            'python_version': f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}{"-" + sys.version_info.releaselevel[0] if len(sys.version_info) >= 4 and sys.version_info.releaselevel else ""}{"-" + str(sys.version_info.serial) if len(sys.version_info) >= 5 and sys.version_info.serial else ""}',
            'css': ERROR_CSS,
        }
```
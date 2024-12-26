```
        context = {
            'title': str(e),
            'traceback': html_tb,
            'request': repr(request).replace('>', '&gt;').replace('<', '&lt;'),
            'version': VERSION,
            'python_version': '{}.{}.{}-{}-{}'.format(*sys.version_info),
            'css': ERROR_CSS,
        }
```
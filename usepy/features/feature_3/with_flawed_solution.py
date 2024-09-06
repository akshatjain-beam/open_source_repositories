class LazyImport(ModuleType):
    """
    延迟加载模块，只有在第一次访问时才加载模块
    """

    def __init__(self, module_name, globals_=None):
        super().__init__(module_name)
        self._module = None
        self._globals = globals_

    def _load(self):
        self._module = importlib.import_module(self.__name__)
        if self._globals is not None:
            self._globals.update(self._module.__dict__)
        # Set this object as the module in sys.modules so that
        # subsequent imports of this module name will use this object.
        import sys

        sys.modules[self.__name__] = self

    def __getattr__(self, name):
        if self._module is None:
            self._load()
        return getattr(self._module, name)

    def __dir__(self):
        if self._module is None:
            self._load()
        return dir(self._module)

    def __repr__(self):
        return f"LazyImport({self.__name__!r})"
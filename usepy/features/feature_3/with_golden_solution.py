class LazyImport(ModuleType):
    def __init__(self, name, module_globals=None):
        if module_globals is None:
            module_globals = globals()
        self._mod_name = name
        self._module_globals = module_globals
        super(LazyImport, self).__init__(name)

    def _load(self):
        module = importlib.import_module(self.__name__)
        self._module_globals[self._mod_name] = module
        self.__dict__.update(module.__dict__)
        return module

    def __getattr__(self, item):
        return getattr(self._load(), item)

    def __dir__(self):
        return dir(self._load())

    def __repr__(self):
        return f"<LazyImport {self.__name__}>"

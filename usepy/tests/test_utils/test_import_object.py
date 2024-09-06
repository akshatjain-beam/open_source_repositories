import pytest
import threading
from usepy import useLazyImport as LazyImport


# Test the LazyImport class
def test_lazy_import_basic():
    lazy_sys = LazyImport('sys')
    assert isinstance(lazy_sys, LazyImport)

def test_lazy_import_access_attribute():
    lazy_sys = LazyImport('sys')
    assert lazy_sys.version_info.major >= 3

def test_lazy_import_access_method():
    lazy_math = LazyImport('math')
    assert lazy_math.sqrt(4) == 2

def test_lazy_import_load_once():
    lazy_sys = LazyImport('sys')
    first_load = lazy_sys._load()
    second_load = lazy_sys._load()
    assert first_load is second_load

def test_lazy_import_dir():
    lazy_sys = LazyImport('sys')
    assert 'version_info' in dir(lazy_sys)

def test_lazy_import_not_existing_module():
    lazy_non_existing = LazyImport('non_existing_module')
    with pytest.raises(ModuleNotFoundError):
        _ = lazy_non_existing.some_attribute

def test_lazy_import_multiple_instances():
    lazy_sys1 = LazyImport('sys')
    lazy_sys2 = LazyImport('sys')
    assert lazy_sys1.version_info is lazy_sys2.version_info

def test_lazy_import_thread_safety():
    def access_lazy_import(lazy_import, results, index):
        results[index] = lazy_import.version_info

    lazy_sys = LazyImport('sys')
    results = [None] * 10
    threads = [threading.Thread(target=access_lazy_import, args=(lazy_sys, results, i)) for i in range(10)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    first_result = results[0]
    for result in results:
        assert result is first_result

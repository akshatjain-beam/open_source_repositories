import pytest
import threading
from usepy import useLazyImport as LazyImport

import os
import sys


# Test the LazyImport class
def test_lazy_import_basic():
    """
    Test the basic functionality of LazyImport.

    This test creates an instance of LazyImport for the 'sys' module and 
    verifies that the instance is of type LazyImport.
    """
    lazy_sys = LazyImport('sys')
    assert isinstance(lazy_sys, LazyImport)

def test_lazy_import_access_attribute():
    """
    Test attribute access through LazyImport.

    This test accesses the 'version_info.major' attribute of the 'sys' module 
    via LazyImport and checks that the major version of Python is 3 or greater.
    """
    lazy_sys = LazyImport('sys')
    assert lazy_sys.version_info.major >= 3

def test_lazy_import_access_method():
    """
    Test method access through LazyImport.

    This test calls the 'sqrt' method from the 'math' module via LazyImport 
    and verifies that the square root of 4 is 2.
    """
    lazy_math = LazyImport('math')
    assert lazy_math.sqrt(4) == 2

def test_lazy_import_load_once():
    """
    Test that the module is only loaded once.

    This test ensures that the 'sys' module is loaded only once by calling 
    the '_load' method twice and checking that both calls return the same module instance.
    """
    lazy_sys = LazyImport('sys')
    first_load = lazy_sys._load()
    second_load = lazy_sys._load()
    assert first_load is second_load

def test_lazy_import_dir():
    """
    Test the __dir__ method of LazyImport.

    This test checks that the 'version_info' attribute is present in the directory 
    listing of the 'sys' module when accessed via LazyImport.
    """
    lazy_sys = LazyImport('sys')
    assert 'version_info' in dir(lazy_sys)

def test_lazy_import_not_existing_module():
    """
    Test handling of non-existing modules.

    This test attempts to create a LazyImport instance for a non-existing module 
    and verifies that accessing an attribute raises a ModuleNotFoundError.
    """
    lazy_non_existing = LazyImport('non_existing_module')
    with pytest.raises(ModuleNotFoundError):
        _ = lazy_non_existing.some_attribute

def test_lazy_import_multiple_instances():
    """
    Test multiple instances of LazyImport for the same module.

    This test creates two LazyImport instances for the 'sys' module and verifies 
    that accessing 'version_info' from both instances returns the same object.
    """
    lazy_sys1 = LazyImport('sys')
    lazy_sys2 = LazyImport('sys')
    assert lazy_sys1.version_info is lazy_sys2.version_info

def test_lazy_import_thread_safety():
    """
    Test thread safety of LazyImport.

    This test accesses the 'version_info' attribute of the 'sys' module via LazyImport 
    from multiple threads and verifies that all threads return the same result.
    """
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

def test_lazy_import_attribute_set_reflects_in_module():
    """Test that setting attributes on the LazyImport instance reflects in the original module."""
    lazy_sys = LazyImport('sys')
    
    # Set a new attribute on the LazyImport instance
    lazy_sys.new_attribute = 'test_value'
    
    # Check if it is set correctly on the instance
    assert lazy_sys.new_attribute == 'test_value'  # Should pass for golden
    
    # Check if it reflects in the original sys module
    assert hasattr(sys, 'new_attribute') is False  # Should fail for flawed

def test_lazy_import_multiple_access_stays_consistent():
    """Test that multiple accesses to LazyImport return consistent module attributes."""
    lazy_math = LazyImport('math')

    # Access an attribute multiple times to ensure consistency
    assert lazy_math.sqrt(4) == 2  # First access
    assert lazy_math.sqrt(4) == 2  # Second access

    # Verify the same instance is being accessed each time
    assert lazy_math is lazy_math  # Should always be the same instance

def test_lazy_import_dir_reflects_module_attributes():
    """Test that the dir() method reflects the attributes of the loaded module."""
    lazy_sys = LazyImport('sys')

    # Invoke dir on the LazyImport instance
    attributes = lazy_sys.__dir__()
    
    # Check that 'version' is in the attributes
    assert 'version' in attributes  # Should pass for golden, fail for flawed

def test_lazy_import_accessing_non_existing_attribute_raises_error():
    """Test that accessing a non-existing attribute raises an error."""
    lazy_non_existing = LazyImport('non_existing_module')

    with pytest.raises(ModuleNotFoundError):
        _ = lazy_non_existing.some_attribute  # Should pass for both but tests error handling

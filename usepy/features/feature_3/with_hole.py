# -*- coding: utf-8 -*-
"""
@Author  : miclon
@Time    : 2022/9/6
@Desc    : 字符串导入模块
@Example
    process:
    import_object('this')

    output:
    The Zen of Python, by Tim Peters
    ……

"""
import functools
import importlib
from types import ModuleType


def import_object(value: str):
    """
    字符串动态导入模块
    :param value: 字符串路径
    :return:
    """
    modname, var = value, None
    if ":" in value:
        modname, var = value.split(":", 1)

    module = importlib.import_module(modname)
    if var is not None:
        var_lst = var.split(".")
        try:
            return module, functools.reduce(getattr, var_lst, module)
        except AttributeError:
            raise ImportError("Module %r does not define a %r variable." % (modname, var)) from None
    return module, None


# - Create a class `LazyImport` to enable loading modules only when they're first accessed.
# - Initialization:
#     - The class should accept a module name and optionally the module's globals dictionary during initialization.
# - Module Loading:
#     - Implement a `_load` method to handle the actual module import, update the module's globals, and set its attributes.
# - Attribute Access:
#     - Override `__getattr__` to trigger the module load and return the requested attribute.
#     - Override `__dir__` to return the list of attributes from the loaded module.
# - Representation:
#     - Implement `__repr__` to give a string representation of the `LazyImport` instance.
$PlaceHolder$
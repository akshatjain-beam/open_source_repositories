from usepy import (
    useCachedProperty,  # noqa
    useCatchError,
    useListify,
    useRunInThread,
    useSingleton,
    useTimeIt,
)

import threading

def test_cached_property():
    class Foo(object):
        @useCachedProperty
        def bar(self):
            return 1

    foo = Foo()
    assert foo.bar == 1
    assert foo.bar == 1


def test_catch_error():
    @useCatchError()
    def foo():
        raise Exception('foo')

    @useCatchError(return_val=1)
    def foo2():
        raise Exception('foo2')

    assert foo() is None
    assert foo2() == 1


def test_listify():
    @useListify()
    def foo():
        yield 1

    @useListify()
    def foo2():
        yield 1
        yield 2

    @useListify(dict)
    def foo3():
        yield 'a', 1
        yield 'b', 2

    assert foo() == [1]
    assert foo2() == [1, 2]
    assert foo3() == {'a': 1, 'b': 2}


def test_run_in_thread():
    @useRunInThread
    def foo():
        return 1

    assert foo() is None


def test_singleton():
    @useSingleton
    class Foo(object):
        pass

    foo = Foo()
    foo2 = Foo()
    assert foo is foo2

def test_single_instance():
    @useSingleton
    class MyClass:
        def __init__(self, value):
            self.value = value

    # Create two instances of MyClass
    instance1 = MyClass(1)
    instance2 = MyClass(2)

    # Check that both instances are the same
    assert instance1 is instance2
    assert instance1.value == 1
    assert instance2.value == 1

def test_thread_safety():
    @useSingleton
    class MyClass:
        def __init__(self, value):
            self.value = value

    # Define a function to create an instance
    def create_instance(results, index, value):
        results[index] = MyClass(value)

    # Store results from multiple threads
    results = [None] * 10

    # Create multiple threads
    threads = [threading.Thread(target=create_instance, args=(results, i, 0)) for i in range(10)]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Check that all results are the same instance
    for result in results:
        assert result is results[0]
        assert result.value == 0

def test_timeit():
    @useTimeIt
    def foo():
        return 1

    assert foo() == 1

import asyncio
import pytest
from supplies.annotate import Annotate, Conotate, Get, update

__author__ = 'dwae'


def test_simple():
    class An(Annotate):
        pass

    @An
    def foo():
        return 42

    assert isinstance(foo, An)
    assert foo.name == 'foo'
    assert foo.definition() == 42

    def foo():
        pass

    assert An(foo).definition is foo
    assert An()(foo).definition is foo

    @An()
    def bar():
        return 13

    assert isinstance(bar, An)
    assert bar.name == 'bar'
    assert bar.definition() == 13


def test_args():
    class Args(Annotate):
        def __init__(self, definition, a=1, b=2):
            super().__init__(definition)
            self.a = a
            self.b = b

    @Args
    def foo():
        return 42

    assert isinstance(foo, Args)
    assert foo.name == 'foo'
    assert foo.definition() == 42
    assert foo.a == 1
    assert foo.b == 2

    @Args(23, 42)
    def bar():
        return 13

    assert isinstance(bar, Args)
    assert bar.name == 'bar'
    assert bar.definition() == 13
    assert bar.a == 23
    assert bar.b == 42

    @Args(23)
    def foo():
        return 42

    assert isinstance(foo, Args)
    assert foo.a == 23
    assert foo.b == 2

    @Args(b=23)
    def foo():
        return 42

    assert isinstance(foo, Args)
    assert foo.a == 1
    assert foo.b == 23

    @Args(42, b=23)
    def foo():
        return 42

    assert isinstance(foo, Args)
    assert foo.a == 42
    assert foo.b == 23

    @Args()
    def foo():
        return 42

    assert isinstance(foo, Args)
    assert foo.a == 1
    assert foo.b == 2


def test_update():
    class Foo:
        @update
        def baz(self, val):
            return val+1

    foo = Foo()
    foo.baz = 1
    assert foo.baz == 2


def test_conotate():
    class Co(Conotate):
        pass

    @Co
    def foo():
        pass

    assert isinstance(foo, Co)
    assert foo.name == 'foo'
    assert asyncio.iscoroutinefunction(foo.definition)

    @Co()
    def bar():
        pass

    assert isinstance(bar, Co)
    assert bar.name == 'bar'
    assert asyncio.iscoroutinefunction(bar.definition)


def test_fails():
    class NilAttr(Annotate, Get):
        pass

    class Foo:
        @NilAttr
        def bar(self):
            pass

    with pytest.raises(NameError):
        Foo().bar
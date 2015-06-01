import pytest
from supplies.annotate import delay
from supplies.params import param, Params

__author__ = 'dwae'


class Foo(Params):
    @param
    def bar(self, val: (1, 42)=23):
        return val

    @delay
    def bla(self):
        return ...


class Bar(Foo, Params):
    @param
    def baz(self, val: str='f00'):
        return val


def test_basic():
    foo = Foo()
    assert foo.bar == 23

    foo.bar = 1
    assert foo.bar == 1

    foo.bar = 42
    assert foo.bar == 42

    foo = Foo(bar=13)
    assert foo.bar == 13

    foo.bar = 37
    assert foo.bar == 37

    bar = Bar()
    assert bar.bar == 23
    assert bar.baz == 'f00'

    bar = Bar(baz='')
    assert bar.bar == 23
    assert bar.baz == ''

    bar = Bar(bar=6)
    assert bar.bar == 6
    assert bar.baz == 'f00'

    bar = Bar(bar=12, baz='foo')
    assert bar.bar == 12
    assert bar.baz == 'foo'

    bar.bar = 2
    bar.baz = 'to'

    assert bar.bar == 2
    assert bar.baz == 'to'

    with pytest.raises(TypeError):
        Bar(bar=1, nil=None)


def test_export():
    bar = Bar(bar=42, baz='foo')

    params = bar.params
    assert {'bar', 'baz'} == params.names

    assert params.bar.name == 'bar'
    assert params['baz'].name == 'baz'

    assert params['bar'].value == 42
    assert params.baz.value == 'foo'

    assert params.bar.default == 23
    assert params.baz.default == 'f00'

    assert 'bar=42' in str(bar)
    assert "baz='foo'" in repr(bar)

    assert bar.bla is ...
    with pytest.raises(KeyError):
        params['bla']

    with pytest.raises(AttributeError):
        params.bla


class Convert(Params):
    @param
    def a(self, val=1):
        return int(val)

    @param
    def b(self, val=''):
        return str(val)


def test_convert():
    conv = Convert()
    assert conv.a == 1
    assert conv.b == ''

    conv = Convert(a='13', b=37)
    assert conv.a == 13
    assert conv.b == '37'

    conv.a = '42'
    assert conv.a == 42
    conv.b = None
    assert conv.b == str(None)


class Dependent(Params):
    @param
    def a(self, val=1):
        return val

    @param
    def b(self, val=None):
        if val is None:
            return self.a + 1
        else:
            return val

    @param
    def c(self, val):
        return self.a + val

    @param
    def d(self, val=3):
        return self.a + val


def test_depend():
    dep = Dependent()

    assert dep.a == 1
    assert dep.b == 2

    dep.a = 2
    assert dep.a == 2
    assert dep.b == 3

    dep.a = 1
    assert dep.a == 1
    assert dep.b == 2

    dep.b = 4
    dep.a = 5
    assert dep.a == 5
    assert dep.b == 4

    dep.c = 3
    assert dep.c == 8

    dep.a = 3
    dep.b = 2
    assert dep.c == 6

    assert dep.b == 2
    del dep.b
    assert dep.b == 4

    del dep.a
    assert dep.b == 2

    del dep.c
    with pytest.raises(TypeError):
        dep.c

    assert dep.d == 4
    dep.a = 3
    assert dep.d == 6
    del dep.a
    assert dep.d == 4

    dep.d = 4
    assert dep.d == 5
    dep.a = 4
    assert dep.d == 8
    del dep.d
    assert dep.d == 7
    del dep.a
    assert dep.d == 4

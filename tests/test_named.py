__author__ = 'dwae'

from supplies.coop import Named


class A:
    def __init__(self, param1, param2=None):
        self.param1 = param1
        self.param2 = param2


class NamedA(Named, A):
    pass


def test_names():
    foo = NamedA(6, name='foo')
    assert str(foo) == 'foo'
    assert repr(foo).endswith(' (foo)')

    assert foo.name == 'foo'
    assert foo.param1 == 6
    assert foo.param2 is None

    bar = NamedA('a', 42, name='bar')
    assert bar.name == 'bar'
    assert bar.param1 == 'a'
    assert bar.param2 == 42

    baz = NamedA(13, name='baz', param2=37)
    assert baz.name == 'baz'
    assert baz.param1 == 13
    assert baz.param2 == 37

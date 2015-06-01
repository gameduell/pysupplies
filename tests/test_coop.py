from supplies import Co

__author__ = 'wabu'


class A:
    def foo(self):
        return 'a', self.bar()

    def bar(self):
        raise NotImplementedError()


class B:
    def bar(self):
        return 'b'


class C:
    def bar(self):
        return 'c'


def test_coop():
    ab = Co[B, A]()
    ac = Co[C, A]()
    abc = Co[C, B, A]()

    assert isinstance(ab, A)
    assert isinstance(ab, B)

    assert isinstance(ac, A)
    assert isinstance(ac, C)

    assert isinstance(abc, A)
    assert isinstance(abc, B)
    assert isinstance(abc, C)

    assert ab.foo() == ('a', 'b')
    assert ac.foo() == ('a', 'c')

    assert abc.bar() == 'c'
    assert abc.foo() == ('a', 'c')

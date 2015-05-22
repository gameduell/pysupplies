from supplies.annotate import attr, delay, refer

__author__ = 'dwae'


class Test:
    def __init__(self, cnt=0):
        self.cnt = cnt

    @attr
    def foo(self):
        cnt = self.cnt
        self.cnt += 1
        return cnt

    @delay
    def bar(self):
        cnt = self.cnt
        self.cnt += 1
        return cnt

    @refer
    def baz(self):
        cnt = self.cnt
        self.cnt += 1
        return cnt


def test_attr():
    assert isinstance(Test.foo, attr)

    t = Test()

    assert t.foo == 0
    assert t.foo == 1

    t.foo = 42

    assert t.foo == 42
    assert t.foo == 42

    assert t.bar == 2
    assert t.bar == 2

    del t.foo

    assert t.foo == 3
    assert t.foo == 4
    assert t.bar == 2

    del t.bar

    assert t.bar == 5
    assert t.bar == 5
    assert t.foo == 6

    assert t.baz == 7
    assert t.baz == 7

    import pickle
    t_ = pickle.loads(pickle.dumps(t))

    assert t.foo == 8
    assert t_.foo == 8

    assert t.bar == 5
    assert t_.bar == 5

    assert t.baz == 7
    assert t_.baz == 9

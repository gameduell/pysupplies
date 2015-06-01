__author__ = 'wabu'


from supplies.strings import uncamel, splitcamel, abbrev, nameof


def test_uncamel():
    assert uncamel('HTTPRequestHeader') == 'http-request-header'
    assert uncamel('StatusCode404Error', sep=' ') == 'status code 404 error'


def test_splitcamel():
    assert splitcamel('ATestClass') == ['a', 'test', 'class']
    assert splitcamel('13TestStr') == ['13', 'test', 'str']


class GameDuell:
    def __init__(self):
        self.name = 'FooBar'


def test_nameof():
    assert nameof('ANot soFancy string') == 'a-not-so-fancy-string'
    assert nameof('a:fancy%split string', sep='.') == 'a:fancy%split.string'
    assert nameof(GameDuell) == 'game-duell'
    assert nameof(GameDuell()) == 'FooBar'


def test_abbrev():
    assert abbrev('GameDuell 4 Ever') == 'gmdllvr'

    assert abbrev('GameDuell 4 Ever', 3) == 'gmd'

    assert abbrev(GameDuell) == 'gmdll'
    assert abbrev(GameDuell()) == 'FBr'

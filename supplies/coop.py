from collections import Counter
import weakref
from supplies.strings import splitcamel


class Named:
    def __init__(self, *args, name, **kws):
        super().__init__(*args, **kws)
        self.name = name

    def __repr__(self):
        r = super().__repr__()
        return '{} ({})'.format(r, self.name)

    def __str__(self):
        return self.name


class _Co(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls.__cache__ = weakref.WeakValueDictionary()

    def __getitem__(cls, classes):
        typ = cls.__cache__.get(classes)
        if not typ:
            names = []
            for typ in classes:
                names.extend(splitcamel(typ.__name__))

            included = set()
            less = []
            for name in reversed(names):
                if name not in included:
                    less.insert(0, name)
                    included.add(name)

            name = ''.join(map(str.capitalize, less))

            typ = type(name, classes, {})
            cls.__cache__[classes] = typ
        return typ


class Co(metaclass=_Co):
    pass
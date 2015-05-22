from supplies.annotate import Update, Attr, delay
from supplies.depend import Depend

__author__ = 'dwae'
__all__ = ['param', 'Params']


class Param(Depend, Attr, Update):
    """
    Annotation for parameter definition
    """


param = Param


class Parameter:
    def __init__(self, descr, instance):
        self.descr = descr
        self.instance = instance

    @property
    def name(self):
        return self.descr.name

    @property
    def value(self):
        return self.descr.__get__(self.instance)

    @property
    def default(self):
        return self.descr.definition(self.instance)

    def __str__(self):
        return '{}={!r}'.format(self.name, self.value)

    __repr__ = __str__


class Parameters:
    def __init__(self, instance):
        self.instance = instance

    @delay
    def names(self):
        return {p.name for p in Param.iter(self.instance)}

    def __getitem__(self, item):
        descr = getattr(type(self.instance), item, None)

        if not isinstance(descr, Param):
            raise KeyError('No parameter {!r} for {} object'.format(
                item, type(self).__name__))

        return Parameter(descr, self.instance)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as e:
            raise AttributeError(*e.args)

    def __str__(self):
        return '{}[{}]'.format(type(self.instance).__name__,
                               ', '.join(str(self[p]) for p in self.names))

    def __repr__(self):
        return '{}[{}]'.format(type(self.instance).__name__,
                               ', '.join(repr(self[p]) for p in self.names))


class Params:
    """
    Mixin for parameter management
    """
    def __init__(self, **kwargs):
        for p in Param.iter(self):
            if p.name in kwargs:
                p.__set__(self, kwargs.pop(p.name))
        super().__init__(**kwargs)

    @delay
    def params(self):
        return Parameters(self)

    def __str__(self):
        return str(self.params)

    def __repr__(self):
        return repr(self.params)

from supplies.annotate import Delay, Update, Attr
from supplies.depend import Depend

__author__ = 'dwae'
__all__ = ['param', 'Params']


class Param(Depend, Attr, Update):
    """
    Annotation for parameter definition
    """


param = Param


class Params:
    """
    Mixin for parameter management
    """
    def __init__(self, **kwargs):
        for p in Param.iter(self):
            if p.name in kwargs:
                p.__set__(self, kwargs.pop(p.name))
        super().__init__(**kwargs)

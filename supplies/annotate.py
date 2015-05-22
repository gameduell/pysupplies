from functools import wraps
import weakref

from asyncio import coroutine

from supplies.coop import Named


__author__ = 'dwae'
__all__ = ['delay', 'refer', 'update', 'attr']


class Annotate(Named):
    """
    The Annotate class wraps an annotated class or function into an object
    """
    def __new__(cls, *args, **kws):

        if len(args) == 1 and not kws:
            definition, = args
            if hasattr(definition, '__name__'):
                return wraps(definition)(super().__new__(cls))

        sup = super()

        def annotate(f):
            self = wraps(f)(sup.__new__(cls))
            self.__init__(f, *args, **kws)
            return self
        return annotate

    def __init__(self, definition):
        super().__init__(name=definition.__name__)
        self.definition = definition

    def call(self, *args, **kws):
        return self.definition(*args, **kws)

    @classmethod
    def iter(cls, instance, owner=None):
        typ = owner or type(instance)
        for name in dir(typ):
            desc = getattr(typ, name)
            if isinstance(desc, cls):
                yield desc


class Conotate(Annotate):
    """
    The Conotate mixin for Annotate wraps its definition with asyncio.coroutine
    """
    def __init__(self, definition, *args, **kws):
        super().__init__(coroutine(definition), *args, **kws)


class Descriptor:
    """
    Base class to define binding behaviour for descriptors
    """
    def lookup(self, instance):
        return {}, None

    def has_entry(self, instance):
        dct, key = self.lookup(instance)
        return key in dct

    def get_entry(self, instance):
        dct, key = self.lookup(instance)
        return dct[key]

    def set_entry(self, instance, val):
        dct, key = self.lookup(instance)
        dct[key] = val

    def del_entry(self, instance):
        dct, key = self.lookup(instance)
        del dct[key]


class ObjDescriptor(Descriptor, Named):
    """
    The ObjDescr mixin stores values into objects __dict__.
    """
    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.entry = '_'+self.name

    def lookup(self, instance):
        return instance.__dict__, self.entry


class RefDescriptor(Descriptor):
    """
    The RefDscr mixin associates values weakly to objects in it's own dict
    """
    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.refs = weakref.WeakKeyDictionary()

    def lookup(self, instance):
        return self.refs, instance


class Get(Descriptor):
    """
    Get mixin supports getting values from the descriptor
    """
    def __get__(self, instance, owner=None):
        if instance is None:
            return self

        if self.has_entry(instance):
            return self.get_entry(instance)
        else:
            return self.__default__(instance)

    def __default__(self, instance):
        raise NameError("Descriptor {} of {} object has no associated value"
                        .format(self, type(instance).__name__))


class Property(Get, Annotate):
    """
    Property mixin calls the definition to get a value
    """
    def __default__(self, instance):
        return self.call(instance)


class Set(Descriptor):
    """
    Set mixin supports setting and deleting values from the descriptor
    """

    def __set__(self, instance, value):
        self.set_entry(instance, value)

    def __delete__(self, instance):
        self.del_entry(instance)


class Update(Get, Set, Annotate):
    """
    Update mixin calls the definition with the supplied value when set
    """
    def __set__(self, instance, val):
        val = self.call(instance, val)
        super().__set__(instance, val)


class _Update(Update, ObjDescriptor):
    pass


update = _Update


class Cache(Get, Set):
    """
    Cache mixin calls it's definition only once, storing the return value
    """
    def __default__(self, instance):
        val = super().__default__(instance)
        self.set_entry(instance, val)
        return val


class Attr(Property, ObjDescriptor, Set):
    """
    @attr descriptors allow setting a value but call definition by default
    """
    pass


attr = Attr


class Delay(Cache, Attr):
    """
    @delay descriptors call definition when needed
    and store the returned value
    """
    pass


delay = Delay


class Refer(Cache, Property, RefDescriptor, Get, Set):
    """
    @refer descriptors call definition when needed and
    refer to there value reference by the object
    """
    pass


refer = Refer

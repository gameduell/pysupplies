from contextlib import contextmanager
import weakref
from supplies.annotate import Get, Set, Annotate, Cache, Attr

__author__ = 'dwae'
__all__ = ['depend']


class Dependent:
    """
    instance of an dependency track descriptor value
    """
    __traces__ = []

    def __init__(self, descr, instance, influencing=None):
        self.descr = descr
        self.instance = instance
        if influencing is None:
            influencing = weakref.WeakSet()
        self.influencing = influencing

        self.value = ()

    @contextmanager
    def trace(self):
        """
        activates tracing of dependencies for this value
        """
        try:
            self.__traces__.append(self)
            yield
        finally:
            tr = self.__traces__.pop()
            assert tr == self

    def access(self):
        """
        specifies that the value is accessed
        """
        for tr in self.__traces__:
            if tr != self:
                self.influencing.add(tr)

    def invalidates(self):
        """
        invalidates the value
        """
        self.value = ()
        for inf in self.influencing:
            if inf.descr.has_entry(inf.instance):
                inf.descr.del_entry(inf.instance)


def _insert_dep(f):
    """
    this annotation inserts a Dependent parameter for the given instance
    """
    def dependent(self, instance, *args, **kws):
        if instance is None:
            dep = None
        else:
            try:
                dep = self.dependents[instance]
            except KeyError:
                dep = Dependent(self, instance)
                self.dependents[instance] = dep
        return f(self, dep, instance, *args, **kws)
    return dependent


class Depend(Get, Set, Annotate):
    """
    Annotation to define dependency traced descriptors
    """
    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.dependents = weakref.WeakKeyDictionary()

    @_insert_dep
    def call(self, dep, *args, **kws):
        with dep.trace():
            return super().call(*args, **kws)

    @_insert_dep
    def __get__(self, dep, instance, owner=None):
        if instance is None:
            return super().__get__(instance, owner)

        dep.access()
        return super().__get__(instance, owner)

    @_insert_dep
    def __set__(self, dep, instance, value):
        dep.invalidates()
        result = super().__set__(instance, value)
        dep.value = (value,)
        return result

    @_insert_dep
    def __delete__(self, dep, instance):
        dep.invalidates()
        dep.value = ()
        if self.has_entry(instance):
            super().__delete__(instance)

    @_insert_dep
    def __default__(self, dep, instance):
        if dep.value:
            self.__set__(instance, dep.value[0])
            return super().__get__(instance)
        else:
            return super().__default__(instance)


class _Depend(Depend, Cache, Attr):
    pass


depend = _Depend

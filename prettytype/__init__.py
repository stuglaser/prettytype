from itertools import izip
import numbers


class NoneT(object):
    def __repr__(self):
        return 'NoneT()'

    def __str__(self):
        return 'None'

    def msct(self, other):
        if isinstance(other, NoneT):
            return self
        return MaybeT(other)


class MaybeT(object):
    def __init__(self, childT):
        self.childT = childT

    def __repr__(self):
        return 'MaybeT({!r})'.format(self.childT)

    def __str__(self):
        return str(self.childT) + '?'

    def __eq__(self, other):
        return isinstance(other, MaybeT) and self.childT == other.childT

    def __neq__(self, other):
        return not self == other

    def msct(self, other):
        if isinstance(other, MaybeT):
            return MaybeT(self.childT.msct(other.childT))
        elif isinstance(other, NoneT):
            return self
        else:
            return MaybeT(self.childT.msct(other))


class AnyT(object):
    def parent(self):
        return None

    def __repr__(self):
        return 'AnyT()'

    def __str__(self):
        return '*'

    def msct(self, other):
        if isinstance(other, NoneT):
            return MaybeT(self)
        return self
anyT = AnyT()


class SimpleType(object):
    def __init__(self, name, parent=anyT, type=None):
        self.name = name
        self._parent = parent
        self.type = type

    def parent(self):
        return self._parent

    def ancestry(self):
        anc = [self]
        t = self
        while True:
            t = t.parent()
            if t is None:
                break
            anc.append(t)
        anc.reverse()
        return anc

    def msct(self, other):
        if isinstance(other, SimpleType):
            if self.name == other.name:
                return self
            # Finds a common ancestor
            best = anyT
            for aT, bT in izip(self.ancestry(), other.ancestry()):
                if aT != bT:
                    break
                best = aT
            return best
        elif isinstance(other, NoneT):
            return other.msct(self)
        else:
            return anyT

    def __repr__(self):
        return 'SimpleType(%r, %r, %r)' % (self.name, self._parent, self.type)

    def __str__(self):
        return self.name

emptyT = SimpleType('')
noneT = NoneT()
numberT = SimpleType('number')
intT = SimpleType('int', parent=numberT, type=int)
floatT = SimpleType('float', parent=numberT, type=float)
stringT = SimpleType('str', type=basestring)

PRIMITIVES = [intT, floatT, stringT]


class ListT(object):
    def __init__(self, eltT):
        self.eltT = eltT

    def __eq__(self, other):
        return isinstance(other, ListT) and self.eltT == other.eltT

    def __neq__(self, other):
        return not self == other

    def __repr__(self):
        return 'ListT({!r})'.format(self.eltT)

    def __str__(self):
        return '[{}]'.format(self.eltT)

    def msct(self, other):
        if isinstance(other, ListT):
            if self.eltT == other.eltT:
                return self
            return ListT(self.eltT.msct(other.eltT))
        elif isinstance(other, NoneT):
            return other.msct(self)
        else:
            return anyT


class DictT(object):
    def __init__(self, keyT, valueT):
        self.keyT = keyT
        self.valueT = valueT

    def __eq__(self, other):
        return (
            isinstance(other, DictT) and
            self.keyT == other.keyT and
            self.valueT == other.valueT)

    def msct(self, other):
        if isinstance(other, DictT):
            if self.keyT == other.keyT and self.valueT == other.valueT:
                return self
            return DictT(
                self.keyT.msct(other.keyT),
                self.valueT.msct(other.valueT))
        elif isinstance(other, NoneT):
            return other.msct(self)
        else:
            return anyT

    def __repr__(self):
        return 'DictT({!r}, {!r})'.format(self.keyT, self.valueT)

    def __str__(self):
        if self.keyT == self.valueT == emptyT:
            return '{:}'
        return '{%s: %s}' % (self.keyT, self.valueT)


class ClassT(object):
    def __init__(self, class_):
        self.class_ = class_

    def __eq__(self, other):
        return isinstance(other, ClassT) and self.class_ == other.class_

    def __ne__(self, other):
        return not self == other

    def parent(self):
        assert self.class_ != object
        # TODO: Handle multiple inheritance somehow
        return ClassT(self.class_.__bases__[0])

    def ancestry(self):
        anc = []
        t = self
        while t.class_ != object:
            anc.append(t)
            t = t.parent()
        anc.reverse()
        return anc

    def msct(self, other):
        if self == other:
            return self
        elif isinstance(other, ClassT):
            best = anyT
            for aT, bT in izip(self.ancestry(), other.ancestry()):
                if aT != bT:
                    break
                best = aT
            return best
        elif isinstance(other, NoneT):
            return other.msct(self)
        else:
            return anyT

    def __repr__(self):
        return 'ClassT({})'.format(self.class_.__name__)

    def __str__(self):
        return self.class_.__name__


# most specific common type
def msct_all(types):
    if len(types) == 0:
        return emptyT

    best = types[0]
    for t in types[1:]:
        best = best.msct(t)
    return best


def typeof(obj):
    if obj is None:
        return noneT

    for prim in PRIMITIVES:
        if isinstance(obj, prim.type):
            return prim

    if isinstance(obj, list):
        return ListT(msct_all([typeof(x) for x in obj]))
    elif isinstance(obj, dict):
        return DictT(
            msct_all([typeof(k) for k in obj.iterkeys()]),
            msct_all([typeof(v) for v in obj.itervalues()]))
    else:
        return ClassT(type(obj))


def prettytype(obj):
    desc = typeof(obj)
    return str(desc)

    if isinstance(obj, basestring):
        return 'str'
    elif isinstance(obj, tuple):
        return 'todo'
    return ANY

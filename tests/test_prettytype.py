import unittest

from prettytype import *


class TestMSCT(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(intT.msct(intT), intT)
        self.assertEqual(intT.msct(floatT), numberT)

    def test_unrelated(self):
        #self.assertEqual(intT.msct(noneT), anyT)
        self.assertEqual(intT.msct(noneT), MaybeT(intT))
        self.assertEqual(intT.msct(ListT(intT)), anyT)

    def test_inheritance(self):
        class Base(object): pass
        class Foo(Base): pass
        class Bar(Base): pass

        baseT = ClassT(Base)
        fooT = ClassT(Foo)
        barT = ClassT(Bar)

        self.assertEqual(baseT, baseT)
        self.assertEqual(baseT.msct(fooT), baseT)
        self.assertEqual(fooT.msct(barT), baseT)


class TestType(unittest.TestCase):
    def istype(self, x, t):
        return self.assertEqual(typeof(x), t)

    def test_primitives(self):
        self.assertEqual(typeof(34), intT)
        self.assertEqual(typeof(5.6), floatT)
        self.assertEqual(typeof('foobar'), stringT)
        self.assertEqual(typeof(None), noneT)

    def test_lists(self):
        self.istype([], ListT(emptyT))
        self.istype([1, 2, 3], ListT(intT))
        self.istype([1, 2, 3.9, 5], ListT(numberT))
        self.istype([1, 2, None], ListT(MaybeT(intT)))

        self.istype([[], [], []], ListT(ListT(emptyT)))
        self.istype([[1, 2], [3, 4]], ListT(ListT(intT)))
        self.istype([[1, 2, 3], [4.5]], ListT(ListT(numberT)))

        self.istype([[1, 2], 4], ListT(anyT))

    def test_dicts(self):
        self.istype({}, DictT(emptyT, emptyT))
        self.istype({1:1, 2:2}, DictT(intT, intT))
        self.istype({1:1.1, 2:2.2}, DictT(intT, floatT))

        # key/value inheritance
        self.istype({1: 1, 2: 'foo'}, DictT(intT, anyT))
        self.istype({1: 1, 2: 2.2}, DictT(intT, numberT))

    def test_dict_ancestry(self):
        self.istype([{}, {}], ListT(DictT(emptyT, emptyT)))
        self.istype([{1: 1}, {2: 2.2}], ListT(DictT(intT, numberT)))

        self.istype([{'a': [1, 2]}, {'b': [3, 4, 5.5]}],
                    ListT(DictT(stringT, ListT(numberT))))

    def test_class_types(self):
        class Base(object): pass
        class Foo(Base): pass
        class Bar(Base): pass

        self.istype(Foo(), ClassT(Foo))
        self.istype([Foo(), Foo()], ListT(ClassT(Foo)))
        self.istype([Foo(), 34], ListT(anyT))

        self.istype([Foo(), Bar()], ListT(ClassT(Base)))

    def test_maybe(self):
        self.istype([1, 2, None, 3], ListT(MaybeT(intT)))
        self.istype([1, 2, None, 3, 4.4], ListT(MaybeT(numberT)))

        self.istype([[1, 2], [None, None]], ListT(ListT(MaybeT(intT))))

        class Foo(object): pass

        t = typeof([Foo(), None, Foo()])
        self.istype([Foo(), None, Foo()], ListT(MaybeT(ClassT(Foo))))


if __name__ == '__main__':
    unittest.main()

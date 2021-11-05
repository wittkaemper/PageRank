from unittest import TestCase

from hypothesis import given, strategies as st

from Page import Page as p


class TestPage(TestCase):

    def setUp(self) -> None:
        self.pages: dict[str, p] = {
            'a': p('a', 2, ['b', 'c']),
            'b': p('b', 2, ['c', 'a']),
            'c': p('b', 2, ['a', 'b'])
        }

    @given(st.floats(allow_nan=None, allow_infinity=None, min_value=0.1, max_value=1))
    def test_calc_formula(self, ldac):
        for x in self.pages.keys():
            self.assertEqual(self.pages[x].calc_formula(self.pages, ldac), 1)

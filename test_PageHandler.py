import copy as c
from unittest import TestCase

from Page import Page as p
from PageHandler import PageHandler


class TestPageHandler(TestCase):

    def setUp(self) -> None:
        self.pageHandler = PageHandler()

    def test_setUp(self) -> None:
        self.assertIsInstance(self.pageHandler.pages, dict)
        self.assertNotEqual(len(self.pageHandler.pages.keys()), 0)
        for x in self.pageHandler.pages.keys():
            self.assertIsInstance(x, str)
        for x in self.pageHandler.pages.values():
            self.assertIsInstance(x, p)

    def test_calcPageRank(self) -> None:
        safe_start_pages = c.deepcopy(self.pageHandler.pages)
        self.pageHandler.calcPageRank()
        for x in self.pageHandler.pages.items():
            self.assertNotEqual(safe_start_pages[x[0]].pageRank, x[1].pageRank)
            self.assertEqual(safe_start_pages[x[0]].refPages, x[1].refPages)
        safe_start_pages = c.deepcopy(self.pageHandler.pages)
        for x in self.pageHandler.pages.items():
            self.assertEqual(safe_start_pages[x[0]].pageRank, x[1].pageRank)
            self.assertEqual(safe_start_pages[x[0]].refPages, x[1].refPages)

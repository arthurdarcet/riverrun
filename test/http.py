import unittest

from riverrun import http


class TestHttp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = http.App()

    def test_books(self):
        self.app.books()

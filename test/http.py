import riverrun


class TestHttp:
    @classmethod
    def setup_class(cls):
        cls.app = riverrun.http.App()

    def test_books(self):
        self.app.books()

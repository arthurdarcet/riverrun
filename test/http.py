import riverrun


class TestHttp:
    @classmethod
    def setup_class(cls):
        cls.app = riverrun.http.root.App()

    def test_index(self):
        self.app.index()

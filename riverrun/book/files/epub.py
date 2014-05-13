import epub

from . import base


class File(base.File):
    extension = 'epub'

    def __init__(self, infile):
        self._epub = epub.open_epub(infile)
        super().__init__(infile)

    def close(self):
        super().close()
        self._epub.close()

    @property
    def isbn(self):
        return self._epub.opf.metadata.get_isbn()

    @property
    def title(self):
        return self._epub.opf.metadata.titles[0][0]

    @property
    def authors(self):
        return self.prepare_authors(c[0] for c in self._epub.opf.metadata.creators)

    @property
    def description(self):
        return self._epub.opf.metadata.description

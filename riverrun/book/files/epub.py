import epub
import io
import os.path

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

    @property
    def cover(self):
        # same method as https://github.com/kovidgoyal/calibre/blob/master/src/calibre/ebooks/metadata/opf2.py#L524
        try:
            cover = next(filter(
                lambda m: m[0].lower() == 'cover',
                self._epub.opf.metadata.metas,
            ))[1]
        except StopIteration:
            return None
        else:
            href = self._epub.get_item(cover).href
            data = io.BytesIO(self.read(href))
            data.name = os.path.basename(href)
            return data

    def read(self, href):
        return self._epub.read_item(href)

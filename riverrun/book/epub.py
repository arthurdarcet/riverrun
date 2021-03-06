import base64
import epub
import io
import os.path

from .ebook import Ebook


class Epub(Ebook):
    def __init__(self, infile):
        super().__init__(infile)
        self.infile.seek(0)
        self._epub = epub.open_epub(self.infile)

    def close(self):
        self._epub.close()

    @property
    def isbn(self):
        return self._epub.opf.metadata.get_isbn()

    @property
    def title(self):
        return self._epub.opf.metadata.titles[0][0]

    @property
    def authors(self):
        for c in self._epub.opf.metadata.creators:
            author = c[0]
            if ', ' in author:
                f, l = author.split(', ', 1)
                author = l + ' ' + f
            yield author

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
            data = self.read(cover)
            return {
                'extension': data.name.rsplit('.', 1)[1],
                'data': base64.b64encode(data.read()),
            }

    def read(self, id_):
        href = self._epub.get_item(id_).href
        data = io.BytesIO(self._epub.read_item(href))
        data.name = os.path.basename(href)
        return data

    @classmethod
    def convert_from(cls, ebook):
        return cls(ebook.convert_to('epub').infile)


import logging
import os.path

from .. import config
from .. import utils
from .ebook import Ebook
from .epub import Epub


logger = logging.getLogger(__name__)

class Book(utils.Model):
    collection = 'books'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._epub = None
        if 'files' not in self:
            self.files = {}
        if 'authors' not in self:
            self.authors = []

    def _path(self, ext):
        return config.library.format(
            authors=', '.join(sorted(self.authors)),
            title=self.title,
            ext=ext,
        )

    @property
    def cover(self):
        if self.epub is not None:
            return self.epub.cover

    @property
    def epub(self):
        if self._epub is None and 'epub' in self.files:
            self._epub = self.get_ebook('epub')
        return self._epub

    def get_ebook(self, extension):
        if extension in self.files:
            return Ebook(self.files[extension])
        else:
            ebook = self.epub.convert_to(extension)
            self.add_file(ebook)
            self.save()
            return ebook

    def add_file(self, ebook, override=True):
        if ebook.extension in self.files and not override:
            return
        path = self._path(ebook.extension)
        ebook.copy_to(path)
        self.files[ebook.extension] = path


def add_file(input, isbn=None, **kwargs):
    with Ebook(input) as ebook:
        with Epub.convert_from(ebook) as epub:
            if isbn is None:
                isbn = epub.isbn

            if isbn is None:
                raise ValueError('No ISBN found in file {!r}'.format(input))

            book = Book.objects.find_one({'isbn': isbn})
            if book is None:
                book = Book(
                    isbn=isbn,
                    title=epub.title,
                    description=epub.description,
                    authors=list(epub.authors),
                )

            book.add_file(ebook, override=True)
            book.add_file(epub, override=False)
            book.save()

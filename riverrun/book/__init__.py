import logging
import os.path

from .. import config
from .. import utils
from . import files


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
            self._epub = self.get_file('epub')
        return self._epub

    def get_file(self, extension):
        return files.parse(self.files[extension])


def add_file(input, isbn=None, **kwargs):
    with files.parse(input) as ebook:
        if isbn is None:
            isbn = ebook.isbn

        if isbn is None:
            raise ValueError('No ISBN found in file {!r}'.format(input))

        book = Book.objects.find_one({'isbn': isbn})
        if book is None:
            book = Book(
                isbn=isbn,
                title=ebook.title,
                description=ebook.description,
                authors=list(ebook.authors),
            )
        path = book._path(ebook.extension)
        ebook.copy_to(path)
        book.files[ebook.extension] = path
        book.save()

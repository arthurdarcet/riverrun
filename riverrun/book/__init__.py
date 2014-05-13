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

    def path(self, ext):
        return config.library.format(
            authors=', '.join(sorted(self.authors)),
            title=self.title,
            ext=ext,
        )


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
                authors=ebook.authors,
            )
        path = book.path(ebook.extension)
        ebook.copy_to(path)
        if path not in book.files:
            book.files.append(path)
        book.save()

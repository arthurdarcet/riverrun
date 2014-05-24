import logging
import os.path

from .. import config
from .. import utils
from .ebook import Ebook
from .epub import Epub


logger = logging.getLogger(__name__)

class Book(utils.Model):
    collection = 'books'

    @classmethod
    def from_ebook(cls, ebook):
        with Epub.convert_from(ebook) as epub:
            book = Book(
                isbn=epub.isbn,
                title=epub.title,
                description=epub.description,
                authors=list(epub.authors),
            )
            try:
                book = cls.objects.get(**{'files.epub': book._path('epub')})
            except Book.DoesNotExist:
                pass
            if 'cover' not in book:
                book['cover'] = epub.cover
            book.add_file(ebook, override=True)
            book.add_file(epub, override=False)
            return book

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'files' not in self:
            self['files'] = {}
        if 'authors' not in self:
            self['authors'] = []

    def _path(self, ext):
        return config.library.format(
            authors=', '.join(sorted(self['authors'])),
            title=self['title'],
            ext=ext,
        )

    @property
    def epub(self):
        return Epub(self['files']['epub'])

    def get_ebook(self, extension):
        if extension in self['files']:
            return Ebook(self['files'][extension])
        else:
            ebook = self.epub.convert_to(extension)
            self.add_file(ebook)
            self.save()
            return ebook

    def add_file(self, ebook, override=True):
        if ebook.extension in self['files'] and not override:
            return
        path = self._path(ebook.extension)
        ebook.copy_to(path)
        self['files'][ebook.extension] = path

    def save(self):
        if 'isbn' in self and self['isbn'] is None:
            del self['isbn']
        return super().save()

    def to_dict(self):
        return {
            'id': str(self['_id']),
            'title': self['title'],
            'authors': self['authors'],
            'description': self['description'],
        }

    def __repr__(self):
        return '<Book {!r}'.format(self['title'])

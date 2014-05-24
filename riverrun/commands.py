from . import setup
from .book import Book
from .book import Ebook


def http(**kwargs):
    from . import http
    setup() # cherrypy LogManager is very stuborn
    http.start()

def add_file(input, isbn=None, **kwargs):
    with Ebook(input[0]) as ebook:
        try:
            if isbn is None:
                raise Book.DoesNotExist
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            book = Book.from_ebook(ebook)
        else:
            book.add_file(ebook)
    for path in input[1:]:
        with Ebook(path) as ebook:
            book.add_file(ebook)
    book.save()

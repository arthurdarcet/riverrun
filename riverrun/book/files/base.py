import io
import os
import shutil


class File:
    extension = None
    mimetype = None

    def __init__(self, infile):
        if isinstance(infile, io.IOBase):
            infile = infile.name
        self._infile = open(infile, 'rb')

    __enter__ = lambda self: self
    __exit__ = lambda self, type, value, traceback: self.close()

    def close(self):
        self._infile.close()

    @property
    def isbn(self):
        raise NotImplementedError()

    @property
    def title(self):
        raise NotImplementedError()

    @staticmethod
    def prepare_authors(authors):
        for author in authors:
            if ', ' in author:
                f, l = author.split(', ', 1)
                author = l + ' ' + f
            yield author

    @property
    def authors(self):
        raise NotImplementedError()

    @property
    def description(self):
        raise NotImplementedError()

    @property
    def cover(self):
        raise NotImplementedError()

    def copy_to(self, path):
        try:
            os.mkdir(os.path.dirname(path))
        except OSError:
            pass
        with open(path, 'wb') as out:
            self.save(out)

    def save(self, out=None):
        if out is None:
            out = io.BytesIO()
        self._infile.seek(0)
        shutil.copyfileobj(self._infile, out)
        out.seek(0)
        return out

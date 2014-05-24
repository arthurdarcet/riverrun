import io
import os
import sh
import shutil
import tempfile

from .. import config


_convert = sh.Command(config.convert)

_mimetypes = {
    'epub': 'application/epub+zip',
    'mobi': 'application/x-mobipocket-ebook',
}

class Ebook:
    def __init__(self, infile):
        self.infile = open(infile, 'rb') if isinstance(infile, str) else infile

    __enter__ = lambda self: self
    __exit__ = lambda self, type, value, traceback: self.close()

    def close(self):
        self.infile.close()

    @property
    def extension(self):
        return self.infile.name.rsplit('.', 1)[1]

    @property
    def mimetype(self):
        try:
            return _mimetypes[self.extension]
        except KeyError:
            return 'application/octet-stream'

    def convert_to(self, extension):
        if self.extension == extension:
            return self
        tmp = tempfile.NamedTemporaryFile(suffix='.' + extension)
        _convert(self.infile.name, tmp.name)
        return self.__class__(tmp)

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
        self.infile.seek(0)
        shutil.copyfileobj(self.infile, out)
        out.seek(0)
        return out

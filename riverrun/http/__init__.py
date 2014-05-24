import bson
import cherrypy
import functools
import os.path
import requests

from .. import config
from ..book import Book
from . import utils


def book_or_404(_id):
    try:
        _id = bson.ObjectId(_id)
    except bson.errors.InvalidId:
        raise cherrypy.NotFound()
    try:
        return Book.objects.get(_id=_id)
    except Book.DoesNotExist:
        raise cherrypy.NotFound()

class App(utils.BaseApp):
    mount_to = '/'
    static_dir = os.path.join(os.path.dirname(__file__), 'static')

    config = {
        '/': {
            'log.access_log_format': '{h}, {s} "{r}"',
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': static_dir,
            'tools.staticdir.match': r'index.(js|css)',
        },
        '/index': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(static_dir, 'index.html'),
        },
        r'/reader/[a-z0-9]{24}': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(static_dir, 'reader.html'),
        }
    }

    @utils.json_exposed
    def books(self):
        return Book.objects.find()

    @cherrypy.expose
    def cover(self, _id):
        data = book_or_404(_id).cover
        cherrypy.response.headers['Content-Type'] = 'image/' + data.name.rsplit('.', 1)[1]
        return data

    @cherrypy.expose
    def reader(self, _):
        with open(os.path.join(self.static_dir, 'reader.html')) as f:
            return f.read()

    @cherrypy.expose
    @functools.lru_cache()
    def epub_js(self, *args):
        return requests.get('http://futurepress.github.io/epub.js/' + '/'.join(args)).content

    @cherrypy.expose
    def get(self, n):
        _id, extension = n.rsplit('.', 1)
        book = book_or_404(_id)
        with book.get_ebook(extension) as ebook:
            cherrypy.response.headers['Content-Type'] = ebook.mimetype
            return ebook.save()


def start():
    cherrypy.config.update(config.http)
    App().mount()
    cherrypy.engine.start()
    cherrypy.engine.block()

import cherrypy
import os.path

from .. import config
from ..book import Book
from . import utils


class App:
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
    }

    @utils.json_exposed
    def books(self):
        return list(Book.objects.find())


def start(**kwargs):
    cherrypy.config.update(config.http)
    cherrypy.quickstart(App(), config=App.config)

import cherrypy

from . import utils
from ..book import Book


class App(utils.BaseApp):
    mount_to = ''

    @cherrypy.expose
    def index(self):
        return 'OK'

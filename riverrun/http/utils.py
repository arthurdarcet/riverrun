import bson
import cherrypy
import functools
import json
import logging
import traceback


logger = logging.getLogger(__name__)

def json_exposed(fn):
    @cherrypy.expose
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            code = 200
            value = fn(*args, **kwargs)
        except cherrypy.HTTPError as e:
            code = e.code
            value = {'status': e.code, 'error': e.reason}
        except Exception as e:
            msg = '{}: {}'.format(e.__class__.__qualname__, e)
            logger.error(msg)
            logger.debug(traceback.format_exc())
            code = 500
            value = {'status': 500, 'error': msg}
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.status = code
        return json.dumps(value).encode('utf-8')
    return wrapper

def paginated(fn):
    @functools.wraps(fn)
    def wrapper(*args, page=0, **kwargs):
        try:
            page = int(page)
        except TypeError:
            raise cherrypy.NotFound()
        else:
            return fn(*args, **kwargs).skip(page * 30).limit(30)
    return wrapper


class _LogManager(cherrypy._cplogging.LogManager):
    def __init__(self):
        self.error_log = logging.getLogger('cherrypy.error')
        self.access_log = logging.getLogger('cherrypy.access')
        self.access_log_format =  '{h}, {s} "{r}"'

class BaseApp:
    def mount(self):
        app = cherrypy.Application(self, self.mount_to, getattr(self, 'config', {'/': {}}))
        app.log = _LogManager()
        cherrypy.tree.mount(app)

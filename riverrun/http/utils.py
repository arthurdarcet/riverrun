import bson
import cherrypy
import functools
import json
import logging
import traceback


logger = logging.getLogger(__name__)

class JSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs['separators'] = ',', ':'
        super().__init__(*args, **kwargs)
    def default(self, o):
        if isinstance(o, bson.ObjectId):
            return str(o)
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        return super().default(o)

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
        return json.dumps(value, cls=JSONEncoder).encode('utf-8')
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

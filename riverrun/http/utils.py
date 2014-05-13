import bson
import cherrypy
import functools
import json
import logging
import traceback


logger = logging.getLogger(__name__)

class JSONEncoder(json.JSONEncoder):
    def __init__(self):
        super().__init__(separators=(',', ':'))
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
json_encoder = JSONEncoder()


def json_exposed(fn):
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
            logger.error(traceback.format_exc())
            code = 500
            value = {'status': 500, 'error': msg}
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.status = code
        return json_encoder.encode(value).encode('utf8')
    wrapper.exposed = True
    return wrapper

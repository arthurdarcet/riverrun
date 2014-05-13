import cherrypy
import logging

from .. import config
from . import root


logger = logging.getLogger(__name__)

def start(**kwargs):
    cherrypy.config.update(config.http)
    for module in (root,):
        module.App().mount()
    cherrypy.engine.start()
    logger.info('Binded socket to %s:%d', config.http['server.socket_host'], config.http['server.socket_port'])
    cherrypy.engine.block()

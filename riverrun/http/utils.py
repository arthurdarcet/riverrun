import cherrypy


class BaseApp:
    mount_to = None
    def __init__(self):
        if not hasattr(self, 'config'):
            self.config = {}
        self.config.setdefault('/', {})
        self.config['/'].setdefault('log.access_log_format', '{h}, {s} "{r}"')

    def mount(self):
        cherrypy.tree.mount(self, self.mount_to, config=self.config)

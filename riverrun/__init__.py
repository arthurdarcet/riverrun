import logging as _logging
import logging.config as _logging_config
import os.path
import yaml


class _config(dict):
    def load(self, cfg):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', cfg + '.yaml')
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.update(self.create(yaml.load(f)))

    @classmethod
    def create(cls, o):
        if isinstance(o, (list, tuple)):
            return [cls.create(x) for x in o]
        elif isinstance(o, dict):
            return cls({k: cls.create(v) for k, v in o.items()})
        else:
            return o

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(err) from err

    def __setattr__(self, k, v):
        self[k] = v

    def __delattr__(self, k):
        if k in self:
            del self[k]

    def __setitem__(self, k, v):
        super().__setitem__(k, self.create(v))

    def setup(self, args):
        self.load('base')
        self.load(args.config)
        self.debug = args.debug

config = _config()


class logging:
    @staticmethod
    def setup(args):
        log_config = {
            'version': 1,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'clean',
                },
            },
            'formatters': {
                'clean': {
                    'format' : '{asctime} | {name:^31} | {levelname:^8} | {message}',
                    'datefmt' : '%Y-%m-%d %H:%M:%S',
                    'style': '{',
                },
                'machine': {
                    'format' : '{asctime} {name} {levelname} {message!r}',
                    'datefmt' : '%Y-%m-%dT%H:%M:%S',
                    'style': '{',
                }
            },
            'loggers': {
                __name__: {
                    'level': 'DEBUG' if args.debug else 'INFO' if not args.quiet else 'WARNING',
                },
                __name__ + '.timer': {
                    'level': 'INFO',
                },
                'cherrypy.access': {
                    'level': 'INFO' if not args.quiet else 'WARNING',
                },
                'cherrypy.error': {
                    'level': 'WARNING',
                },
            },
            'root': {
                'handlers': ['console'],
            }
        }

        _logging_config.dictConfig(log_config)
        _logging.captureWarnings(True)


def setup(args=None):
    if args is not None:
        config.args = args
        config.setup(args or config.args)
    logging.setup(args or config.args)

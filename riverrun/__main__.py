#!/usr/bin/env python

import logging
import logging.config
import argparse
import sys

from . import book
from . import http
from . import config


parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.add_argument('-d', '--debug', action='store_true', help="Log debug messages", default=False)
parser.add_argument('-q', '--quiet', action='store_true', help="Less verbose output", default=False)
subparsers = parser.add_subparsers()

###
subparse = subparsers.add_parser('http', help='Run the http server (default)')

###
subparse = subparsers.add_parser('add', help='Add a book')
subparse.add_argument('input', type=argparse.FileType('rb'), help='ebook file')
subparse.add_argument('-i', '--isbn', action='store', help="ISBN (optional)", default=None, nargs='?')
subparse.set_defaults(func=book.add_file)


args = parser.parse_args()
config.debug = args.debug
config.quiet = args.quiet

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
        'riverrun': {
            'level': logging.DEBUG if args.debug else logging.INFO if not args.quiet else logging.WARNING,
        },
        'cherrypy': {
            'level': logging.INFO if not args.quiet else logging.WARNING,
            'propagate': False
        },
        'cherrypy.error': {
            'level': logging.WARNING
        },
    },
    'root': {
        'handlers': ['console'],
    }
}

logging.config.dictConfig(log_config)
logging.captureWarnings(True)

if not hasattr(args, 'func'):
    args.func = http.start
sys.exit(args.func(**args.__dict__) or 0)

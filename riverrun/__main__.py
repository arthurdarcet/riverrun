#!/usr/bin/env python

import argparse
import sys

parser = argparse.ArgumentParser(fromfile_prefix_chars='@', description='Default command: http and watch')
parser.add_argument('-c', '--config', action='store', type=argparse.FileType('r'), help="Use this config file on top of the base config", default=None)
parser.add_argument('-d', '--debug', action='store_true', help="Log debug messages", default=False)
parser.add_argument('-q', '--quiet', action='store_true', help="Less verbose output", default=False)
subparsers = parser.add_subparsers()

###
subparse = subparsers.add_parser('http', help='Run the http server')
subparse.set_defaults(command='http')

###
subparse = subparsers.add_parser('watch', help='Watch for new files')
subparse.set_defaults(command='watch')

###
subparse = subparsers.add_parser('add', help='Add a book')
subparse.add_argument('input', type=argparse.FileType('rb'), help='ebook file', nargs='+')
subparse.add_argument('-i', '--isbn', action='store', help="ISBN (optional)", default=None, nargs='?')
subparse.set_defaults(command='add_file')

###
subparse = subparsers.add_parser('ensure-indexes', help='Create the Mongo indexes')
subparse.set_defaults(command='ensure_indexes')

args = parser.parse_args()


from . import setup
setup(args)

from . import commands

sys.exit(getattr(commands, getattr(args, 'command', 'run'))(**args.__dict__) or 0)

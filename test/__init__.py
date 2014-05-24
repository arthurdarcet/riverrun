import os

from riverrun import config
from riverrun import setup

class args:
    config = 'test'
    debug = False
    quiet = True

setup(args)

fixtures = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
os.system('mongorestore --drop -d {} {} 2>&1 > /dev/null'.format(config.mongo.database, os.path.join(fixtures, 'db')))

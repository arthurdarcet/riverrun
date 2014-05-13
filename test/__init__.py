import os.path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import riverrun
import riverrun.book

fixtures = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
db = riverrun.config.mongo.tests
os.system('mongorestore --drop -d {} {} 2>&1 > /dev/null'.format(db, os.path.join(fixtures, 'db')));
riverrun.book.Book.objects.set_connection(db)


from .http import *

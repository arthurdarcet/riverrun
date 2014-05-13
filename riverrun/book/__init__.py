import logging

from .. import utils


logger = logging.getLogger(__name__)

class Book(utils.Model):
    collection = 'books'

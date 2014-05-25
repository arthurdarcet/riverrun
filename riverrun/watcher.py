import logging
import os
import pyinotify

from . import config
from .book import Book
from .book import Ebook


logger = logging.getLogger(__name__)

class ProcessEvent(pyinotify.ProcessEvent):
    def _process(self, path):
        if os.path.isdir(path):
            for p in os.listdir(path):
                self._process(p)
        else:
            logger.debug('Processing %r', path)
            with Ebook(path) as ebook:
                book = Book.from_ebook(ebook)
            book.save()
            logger.info('Added %r to %r', path, book)

    def process_IN_CREATE(self, event):
        self._process(os.path.join(event.path, event.name))


def start():
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, ProcessEvent())
    wm.add_watch(config.watch, pyinotify.IN_CREATE)
    notifier.loop()

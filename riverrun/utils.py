import bson
import pymongo
import pymongo.son_manipulator

from . import config


class SONManipulator(pymongo.son_manipulator.SONManipulator):
    def __init__(self, cls):
        self.cls = cls

    def transform_incoming(self, son, collection):
        son = son.copy()
        for k, v in son.items():
            if isinstance(v, set):
                son[k] = list(v)
            elif isinstance(v, dict):
                son[k] = self.transform_incoming(son, collection)
        return son

    def transform_outgoing(self, son, collection):
        return self.cls(son)


mongo_client = pymongo.MongoClient(config.mongo.host)

class Manager:
    class DoesNotExist(Exception):
        pass

    def __init__(self, cls):
        self.cls = cls
        self.son_manipulator = SONManipulator(cls)
        self.set_connection(config.mongo.database, cls.collection)

    def set_connection(self, database=None, collection=None):
        if database is not None:
            self.database = mongo_client[database]
            self.database.add_son_manipulator(self.son_manipulator)
        self.collection = self.database[collection or self.collection.name]

    def __getattr__(self, k):
        return getattr(self.collection, k)

    def get(self, **kwargs):
        data = self.find_one(kwargs)
        if data is None:
            raise self.DoesNotExist('{} not found for query {}'.format(self.cls.__name__, kwargs))
        else:
            return data


class MetaModel(type):
    def __new__(cls, name, bases, attrs):
        res = super().__new__(cls, name, bases, attrs)
        if 'collection' in attrs:
            res.objects = Manager(res)
        return res


class Model(dict, metaclass=MetaModel):
    def save(self):
        self.objects.save({k: v for k, v in self.items() if not k.startswith('_') or k == '_id'})

    @property
    def _id(self):
        if '_id' not in self:
            self['_id'] = bson.ObjectId()
        return self['_id']

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as err:
            raise AttributeError(err)

    def __setattr__(self, key, val):
        self[key] = val

    def __delattr__(self, key):
        del self[key]

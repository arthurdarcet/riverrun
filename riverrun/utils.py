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
                son[k] = self.transform_incoming(v, collection)
        return son

    def transform_outgoing(self, son, collection):
        return self.cls(son)


mongo_client = pymongo.MongoClient(config.mongo.host)

class Manager:
    def __init__(self, cls):
        self.cls = cls
        database = mongo_client[config.mongo.database]
        database.add_son_manipulator(SONManipulator(cls))
        self.collection = database[cls.collection]
        cls.DoesNotExist = type(cls.__name__ + '.DoesNotExist', (cls.DoesNotExist, ), {})

    def __getattr__(self, k):
        return getattr(self.collection, k)

    def get(self, **kwargs):
        data = self.find_one(kwargs)
        if data is None:
            raise self.cls.DoesNotExist(kwargs)
        else:
            return data

class MetaModel(type):
    def __new__(cls, name, bases, attrs):
        res = super().__new__(cls, name, bases, attrs)
        if 'collection' in attrs:
            res.objects = Manager(res)
        return res

class Model(dict, metaclass=MetaModel):
    class DoesNotExist(Exception):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if '_id' not in self:
            self['_id'] = bson.ObjectId()

    def save(self):
        self.objects.save(self)

    def __hash__(self):
        return hash(self['_id'])

    def __repr__(self):
        return '<{} {!r}>'.format(self.__class__.__name__, self['_id'])

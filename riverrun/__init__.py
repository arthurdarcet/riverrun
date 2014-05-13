import os.path
import yaml


CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')

class obj(dict):
    def __init__(self, d):
        for k, v in d.items():
            self[k] = self.create(v)

    @classmethod
    def create(cls, o):
        if isinstance(o, (list, tuple)):
            return [cls.create(x) for x in o]
        else:
            return cls(o) if isinstance(o, dict) else o

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, k, v):
        self[k] = v

    def __delattr__(self, k):
        if k in self:
            del self[k]

    def __setitem__(self, k, v):
        super().__setitem__(k, self.create(v))


with open(CONFIG_FILE, 'r') as f:
    config = obj.create(yaml.load(f))

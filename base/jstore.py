from herzog.base.argorpc import getbbsfile
from herzog.base.log import logger
import os
import json

class FileJSONStore :

    def __init__(self, filepath) :
        self._filepath = filepath
        self._data = {}
        self.load()

    def load(self) :
        try :
            self.data = json.load(open(self._filepath))
        except IOError :
            logger.warning("Cannot load %r" % self._filepath)
            self.data = {}
        return self.data

    def sync(self) :
        json.dump(self.data, open(self._filepath, 'w'))

    def __getitem__(self, key) :
        return self.data[key]

    def get(self, key, default=None) :
        return self.data.get(key, default)

    def geta(self, key):
        return self.data.get(key, [])

    def gets(self, key):
        return self.data.get(key, '')

    def geto(self, key):
        return self.data.get(key, {})

    def __setitem__(self, key, value) :
        self.data[key] = value
        self.sync()

    def set(self, key, value) :
        self.data[key] = value

    def __delitem__(self, key) :
        del self.data[key]
        self.sync()

    def pop(self, key, value) :
        del self.data[key]

hzd = FileJSONStore(getbbsfile('D.herzog'))

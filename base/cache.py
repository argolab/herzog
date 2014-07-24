from functools import wraps

class CacheManage(dict) :

    def cacheup(self):
        fid = id(f)
        @wraps(f)
        def wrapper(*args, **kwargs) :
            if fid not in self :
                self[fid] = f(*args, **kwargs)
            return self[fid]
        self['r%d' % (id(wrapper))] = fid
        return wrapper

    def cachereset(self, wrapper):
        del self[self['r%d' % id(wrapper)]]

cacher = CacheManage()
cacheup = cacher.cacheup
cachereset = cacher.cachereset
cacheclear = cacher.clear


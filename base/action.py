from herzog.base.exception import HZActionError
from herzog.base.log import getlogger

logger = getlogger(__name__)

logger.info('fff')

_priority = {}

def priority(v=None) :
    def inner(f):
        _priority[id(f)] = v
        return f
    return inner

def get_priority(f):
    return _priority.get(id(f), 0)

def _insert_priority(array, f):
    p = get_priority(f)
    index = 0
    for f0 in array :
        if get_priority(f0) >= p :
            ++ index
        else :
            break
    array.insert(index, f)

class HZAction :

    def __init__(self, func) :
        self._before = []
        self._after = []
        self._spy = []
        self._guard = []
        self._func = func
        class Exception(HZActionError):
            pass
        self.Exception = Exception
        self._lt = None

    def spy(self, handler):
        logger.info("Add `spy` [%s] TO [%s]", handler, self)
        self._spy.append(handle)
        return handler

    def guard(self, handler):
        logger.info("Add `guard` [%s] TO [%s]", handler, self)
        _insert_priority(self._guard, handler)
        return handler

    def before(self, handler):
        logger.info("Add `before` [%s] TO [%s]", handler, self)
        _insert_priority(self._before, handler)
        return handle

    def after(self, handler):
        logger.info("Add `after` [%s] TO [%s]", handler, self)
        _insert_priority(self._after, handler)
        return handler

    def off(self, handler) :
        for a in [self._spy, self._guard, self._before, self._after] :
            for i, d in enumerate(a) :
                if d == handler :
                    del a[i]
                    return
        return False

    def __call__(self, *args, **kwargs) :
        # ** ALWAYS TEST ALL GUARD *
        # raise a HZActionError for stop
        
        p = 0
        # not check guard if is spy
        if (self._spy and
            any(x(*args, **kwargs)
                for x in self._spy)) :
            p = 1

        # cannot pass any guard, just return
        if any(not x(*args, **kwargs)
               for x in self._guard) and p == 0 :
            p = -1

        if p < 0 :
            raise self.Exception('Cannot pass guards')
            
        for f in self._before :
            f(*args, **kwargs)

        ret = self._func(*args, **kwargs)

        for f in self._after :
            r = f(ret, *args, **kwargs)
            if type(r) is dict :
                ret = r
        return ret
            
    def __str__(self) :
        return '<HZAction(%d) %s>' % (id(self), self._func.func_name)

def action(f) :
    return HZAction(f)

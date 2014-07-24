from herzog.base.exception import HZActionError

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
        self._crash = []
        self._spy = []
        self._guard = []
        self._func = func
        class Exception(HZActionError):
            pass
        self.Exception = Exception

    def spy(self, handler):
        self._spy.append(handle)
        return handler

    def guard(self, handler):
        _insertpriority(self._guard, handler)
        return handler

    def before(self, handler):
        _insertpriority(self._before, handler)
        return handle

    def after(self, handler):
        _insertpriority(self._after, handle)
        return handle

    def crash(self, handler):
        _insertpriority(self._crash, handler)
        return handle

    def __call__(self, ctx, *args, **kwargs) :
        try :

            # not check guard if is spy
            if not (self._spy and
                    any(x(ctx, *args, **kwargs)
                        for x in self._spy)) :
                # cannot pass any guard, just return
                if any(not x(ctx, *args, **kwargs)
                       for x in self._guard) :
                    raise self.Exception('Cannot pass guards')
            
            for f in self._before :
                f(ctx, *args, **kwargs)

            self._func(ctx, *args, **kwargs)

            for f in self._after :
                f(ctx, *args, **kwargs)

            return ctx
        except HZActionError as e :
            for f in self._crash :
                f = f(ctx, e)
                if f :
                    return f
            raise e

    def __unicode__(self) :
        return '<HZAction(%d) %s>' % (id(self), self._func.func_name)

def action(f) :
    return Action(f)

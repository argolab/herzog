class Precondition(Exception):

    def __init__(self, name, **kwargs) :
        self.name = name
        self.kwargs = kwargs

    def __str__(self):
        return 'Precondition(%s)' % self.name

class EventServer :

    def __init__(self):
        self._pool = {}
        self._desc = {}
        
    def register(self, event, desc=''):
        self._pool[event] = []
        self._desc[event] = desc

    def bind(self, event, handle=None):
        if event not in self._pool :
            raise ValueError('No such event name')

        # use for decorator
        if not handle :
            def binder(handle):
                self._pool[event].append(handle)
                return handle
            return binder
            
        self._pool[event].append(handle)
        
    def trigger(self, event, **kwargs):
        if event not in self._pool :
            raise ValueError('No such event name')
        for e in self._pool[event] :
            e(**kwargs)

    def off(self, event, handle) :
        for i, h in enumerate(self._pool[event]) :
            if h is handle :
                del self._pool[event][i]
                return

    def help(self, event) :
        return self._desc[event]

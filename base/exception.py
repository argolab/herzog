class HZError(Exception):
    pass

class HZActionError(HZError):
    pass

class FormValidError(HZError):

    def __init__(self, message, **params):
        self.message = message
        self.params = params

    def __str__(self):
        return 'FormValidError<%s> : %s' % (self.params, self.message)

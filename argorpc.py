from json import loads as json_parse
from urllib import urlencode, urlopen

ARGO_PREFIX = 'http://localhost:1996/bbsapi/'

def argo_http(api, param=None, session=None, fromhost=None):

    '''Make a http post request of `ARGO_PREFIX`

    session need dict() and .update function to
     keep session data.'''

    # merge args
    if session :
        args = dict(session)
    else :
        args = {}
    if param :
        args.update(param)
    if fromhost :
        args['fromhost'] = fromhost

    # parase data
    text = urlopen(
        ARGO_PREFIX + api, urlencode(args)
    ).read().decode('utf-8')
    if text[-1] == '!' :
        seq = text.find('\n')
        session.update(json_parse(text[seq+1:-1]))
        return json_parse(text[0:seq])
    return json_parse(text)

class ArgoRPCClicent :

    def __init__(self, session=None, fromhost=None):
        if session is None:
            session = {}
        self._session = session
        self._fromhost = fromhost

all_api = [
    'test',
    'do_test',
    'do_login', 
    'do_logout',
    'utmpnum',
    'queryuser',
    'listmails',
    'showmail',
    'do_sendmail',
    'do_delmail', 
]

for _api in all_api :
    # Use a closure to keep value not ref
    def closure():
        api = _api
        def inner(self, **param):
            return argo_http(api, param, session=self._session,
                             fromhost=self._fromhost)
        inner.func_name = api
        ArgoRPCClicent.__dict__[api] = inner
    closure()

if __name__ == "__main__" :
    cc = ArgoRPCClicent()
    # print cc.test()
    print cc.queryuser(userid='sysop')

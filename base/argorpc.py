from json import loads as json_parse
from urllib import urlencode, urlopen
from herzog.base.log import getlogger

logger = getlogger(__name__)

ARGO_PREFIX = u'http://localhost:1996/bbsapi/'
ROOT_FMT = u'/home/bbs/bbs_home/%s'

_HOME_FMT = ROOT_FMT % 'home/%s/%s/%s'

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
    text = urlopen(ARGO_PREFIX + api, urlencode(args)).read()

    if not text :
        raise Exception('Empty response url[%s] params[%s]' % (
            (ARGO_PREFIX + api), urlencode(args)))
    
    try :
        text = text.decode('utf-8')
    except UnicodeEncodeError as e:
        logger.warning("Cannot decode %r" % text)
        raise e

    #TODO try to catch unicode decode error
    open('rep.txt', 'wb').write(('%s%s?%s\n\n%s' % (
        ARGO_PREFIX.encode('utf8'), api,
        urlencode(args), text)).encode('utf8'))
    
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

def getbbsfile(path):
    return ROOT_FMT % path

def getuserfile(userid, filename):
    return _HOME_FMT % (userid[0].upper(), userid, filename)

all_api = [
    'test',        
    'do_test', 
    'do_login',  #(id, pw) 
    'do_logout',
    'utmpnum',   #(id)
    'queryuser', #(queryuser)
    'listmails', #(num, limit)
    'showmail',  #(start)
    'do_sendmail', #(userid, title, backup, signature, usesignature, randomsig, text, filenum)
    'do_delmail', #(filenum, :filename)
    'do_snd', #(board, title, text, :refile, :signature, :usesignature, :randomsig)
    'do_del', #(board, file)
    'do_edit', #(board, title, file, text)
    'do_man', #(board, mode, boxFILENAME, boxFILENAME, ...)
    'showboard', #(board)
    'allboards',
    'getmessage'
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

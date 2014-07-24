#-*- coding: utf-8 -*-

from herzog.app import jsonify
from herzog.cache import cacheup
from datetime import datetime as dt

def json_success(**params):
    return jsonify(success=1, **params)

def json_error(code, msg, **params):
    return jsonify(error=1, code=code, msg=msg, **params)

def parse_range(k, min, max, default):
    try:
        k = int(k)
    except (TypeError, ValueError):
        return default
    if k < min or k >= max :
        return default

def parse_int(k, default=None):
    try:
        return int(k)
    except (TypeError, ValueError):
        return default

def getnow():
    return dt.now()

@cacheup
def getsysop() :
    try :
        sysops = set(getbbsfile('etc/SYSOPS.herzog').read().split())
    except IOError :
        print 'Cannot load sysops name. Check your BBS_HOME/etc/SYSOP.herzog file'
        sysops = set()
    return sysops

def issysop(userid):
    return x in getsysop()

def gen_summary(content):
    return content and ''.join(content[:400].split('\n')[:2])

def quote(text, userid):
    return (u'\r\n\r\n【 在 %s (%s) 的大作中提到 : 】\r\n: '
            % (userid, userid) + u'\n: '.join(text.strip().split('\n')[:5]))

def quote_title(title):
    if title[:4] != u'Re: ' :
        return u'Re: ' + title[:4]
    return title

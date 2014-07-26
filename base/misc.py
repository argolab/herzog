#-*- coding: utf-8 -*-

from herzog.base.app import jsonify
from herzog.base.cache import cacheup
from herzog.base.argorpc import getbbsfile
from herzog.base.log import getlogger
from datetime import datetime as dt

logger = getlogger(__name__)

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
        logger.warning('Cannot load sysops name. Check your BBS_HOME/etc/SYSOP.herzog file')
        sysops = set()
    return sysops

def issysop(userid):
    return userid in getsysop()

def gen_summary(content):
    if content :
        if len(content) < 180 :
            return content
        else :
            return ''.join(content[:180].split('\n')[:2]) + '...'

def quote(text, userid):
    buf = [u'\r\n\r\n【 在 %s (%s) 的大作中提到 : 】' % (userid, userid)]
    for l in text.strip().splitlines() :
        if len(buf) > 10 :
            buf.append(u'..............（以下省略）')
            break
        if len(l) > 65 :
            for index in range(0, len(l), 65) :
                if len(buf) > 10 :
                    buf.append(u'..............（以下省略）')
                    break
                buf.append(l[index:index+65])                    
        else :
            buf.append(l)
    return u'\r\n: '.join(buf)

def quote_title(title):
    if title[:4] != u'Re: ' :
        return u'Re: ' + title[:15]
    return title

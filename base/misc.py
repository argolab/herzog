#-*- coding: utf-8 -*-

import re
from flask import escape

from herzog.base.app import jsonify
from herzog.base.jstore import hzd
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

def getsysop() :
    return hzd.geta('site:sysop')

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

re_ansi = re.compile('\x1b[\\[\\d;]*[a-zA-Z\s]')
re_quote = re.compile(u'\\s*【 在 .* 的大作中提到\\s*[:：]\\s*】\\s*'.encode('gbk'))

def filter_ansi(text) :
    return re_ansi.sub('', text)

def getfspost(boardname, oldfilename):
    text = filter_ansi(open(getbbsfile(
        "boards/%s/%s" % (boardname, oldfilename))).read())
    # try :
    #     text = filter_ansi(getbbsfile(
    #         "boards/%s/%s" % (boardname, oldfilename)).read())
    # except IOError:
    #     return None
    if not text :
        logger.warning("Empty post??? [%s/%s]", boardname, oldfilename)
        return None
    if not text.startswith('\xb7\xa2\xd0\xc5\xc8\xcb:') :
        logger.warning("Mysterious board post: [%s/%s]", boardname, oldfilename)
        return None
    text = text.splitlines()
    if len(text) > 400 :
        text = text[:400]
    title = text[1][8:][:35]
    owner = text[0].split(' ')[1]
    quoteheader = 0
    for index in range(len(text)-1, -1, -1) :
        line = text[index].strip()
        if not line or line == '--' or line[0] == ':' \
           or line.startswith('\xa1\xf9') :
            continue
        if re_quote.search(line) :
            index -= 1
            quoteheader = 1
        break
    index +=1
    indexj = index
    for indexj in range(index+quoteheader, len(text)) :
        if not text[indexj] or text[indexj][0] != ':' :
            break
    # header, content, quote, tail
    return dict(title=title, owner=owner), '\n'.join(text[4:index]), \
        '\n'.join(text[index:indexj]), '\n'.join(text[indexj:])

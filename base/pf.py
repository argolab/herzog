#-*- coding: utf-8 -*-

def gen_summary(content):
    return content and ''.join(content[:400].split('\n')[:2])

def quote(text, userid):
    return (u'\r\n\r\n【 在 %s (%s) 的大作中提到 : 】\r\n: '
            % (userid, userid) + u'\n: '.join(text.strip().split('\n')[:5]))

def quote_title(title):
    if title[:4] != u'Re: ' :
        return u'Re: ' + title[:4]
    return title

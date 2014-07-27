from herzog.actions.new import topic, reply, comment
from herzog.base import HZActionError
from herzog.base.misc import quote, quote_title
from herzog.base.ctx import getclient, g, getconn

def fixtext(s) :
    return '\r\n'.join(s.splitlines()).encode('utf8')

@topic.guard
def save_topic_to_fs(userid, boardname, title, content,
                     fromaddr, **ps) :
    ret = getclient().do_snd(board=boardname, title=title.encode('utf8'),
                             text=content.encode('utf8'))
    if 'error' in ret :
        raise HZActionError(ret['emsg'])
    g._filename = ret['filename']
    return True

@topic.after
def update_filename_topic(ret, *s, **ps):
    db = getconn()
    db.execute(u" UPDATE herzog_topic SET oldfilename=%s WHERE tid=%s",
               g._filename, ret['tid'])
    ret['filename'] = g._filename

@reply.guard
def save_reply_to_fs(userid, tid, content, fromaddr, **ps):
    origin = getconn().get(u"SELECT boardname, oldfilename, title, content,"
                           "     owner FROM herzog_topic WHERE tid=%s", tid)
    if not origin :
        raise HZActionError("No such topic")
    content = fixtext(content + quote(origin.content, origin.owner))
    print content
    ret = getclient().do_snd(board=origin.boardname,
                             title=quote_title(origin.title).encode('utf8'),
                             text=content,
                             refile=origin.oldfilename)
    if 'error' in ret :
        raise HZActionError(ret['emsg'])
    g._filename = ret['filename']
    return True
    
@comment.guard
def save_comment_to_fs(userid, replyid, content, fromaddr, **ps):
    db = getconn()
    origin = db.get(u"SELECT tid, oldfilename, content, owner"
                           " FROM herzog_reply WHERE rid=%s", replyid)
    if not origin :
        raise HZActionError("ReplyError: No such post")
    content = content + quote(origin.content, origin.owner)
    torigin = db.get(u"SELECT boardname, title FROM herzog_topic"
                     " WHERE tid=%s", origin.tid)
    if not torigin :
        raise Precondition("ReplyError:No such topic")
    ret = getclient().do_snd(board=torigin.boardname,
                             title=quote_title(torigin.title).encode('utf8'),
                             text=content.encode('utf8'),
                             refile=origin.oldfilename)
    if 'error' in ret :
        raise HZActionError(u'Cannot save post. [%s]' % ret['emsg'])
    g._filename = ret['filename']
    return True

@reply.after
@comment.after
def update_filename_reply(ret, *s, **ps):
    db = getconn()
    db.execute(u"UPDATE herzog_reply SET oldfilename=%s WHERE rid=%s",
               g._filename, ret['rid'])
    ret['filename'] = g._filename

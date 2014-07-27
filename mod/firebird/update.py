from herzog.base import getconn, getclient, HZActionError
from herzog.base.misc import getfspost
from herzog.actions.update import update_topic, update_reply

@update_topic.guard
def update2fs(userid, tid, title, content, **ps):
    db = getconn()
    topic = db.get(u"SELECT boardname, oldfilename FROM herzog_topic"
                   "  WHERE tid=%s", tid)
    if not topic :
        raise HZActionError('No such topic')
    r = getclient().do_edit(board=topic.boardname,
                            title=title.encode('utf8'),
                            text=content.encode('utf8'),
                            file=topic.oldfilename)
    if r.has_key('error') :
        raise HZActionError(r['emsg'])
    return True

@update_reply.guard
def update2fs_reply(userid, rid, content, **ps) :
    db = getconn()
    reply = db.get(u"SELECT tid, oldfilename FROM herzog_reply"
                   "  WHERE rid=%s", rid)
    if not reply :
        raise HZActionError('No such reply')
    topic = db.get(u"SELECT boardname FROM herzog_topic"
                   "  WHERE tid=%s", reply.tid)
    if not topic :
        raise HZActionError("No such topic")
    header, _, quote, tail = getfspost(topic.boardname,
                                       reply.oldfilename)
    r = getclient().do_edit(board=topic.boardname,
                            title=header['title'].decode('gbk').encode('utf8'),
                            text=content.encode('utf8'),
                            file=reply.oldfilename)
    if r.has_key('error') :
        raise HZActionError(r['emsg'])
    return True
    

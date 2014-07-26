from herzog.base import action, getconn, HZActionError
from herzog.actions.delete import deltopic, delreply, isowner_topic,\
    isowner_reply

deltopic.off(isowner_topic)
delreply.off(isowner_reply)

@deltopic.guard
def del_fs_topic(tid, **ps) :
    topic = db.GET(u"SELECT oldfilename, boardname FROM herzog_topic"
                   "  WHERE tid=%s", tid)
    if not topic :
        raise HZActionError('No such topic')
    r = getclient().do_del(board=topic.boardname,
                           file=ret.oldfilename)
    if 'error' in r :
        raise HZActionError(r.emsg)
    return True

@delreply.guard
def del_fs_reply(rid, **ps) :
    reply = db.get(u"SELECT tid, oldfilename FROM herzog_reply"
                   "  WHERE rid=%s", rid)
    if not reply :
        raise HZActionError('No such reply')
    topic = db.get(u"SELECT boardname FROM herzog_topic"
                   "  WHERE tid=%s", reply.tid)
    if not topic :
        raise HZActionError('No such topic')
    r = getclient().do_del(board=topic.boardname,
                           file=reply.oldfilename)
    if 'error' in r :
        raise HZActionError(r.emsg)
    return True


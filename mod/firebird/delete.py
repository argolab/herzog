#-*- coding: utf-8 -*-

from herzog.base import action, getconn, HZActionError, getclient, authed, request
from herzog.base.log import getlogger
from herzog.actions.delete import deltopic, delreply, isowner_topic,\
    isowner_reply

deltopic.off(isowner_topic)
delreply.off(isowner_reply)

logger = getlogger(__name__)

@deltopic.guard
def del_fs_topic(userid, tid, **ps) :
    db = getconn()
    topic = db.get(u"SELECT oldfilename, boardname FROM herzog_topic"
                   "  WHERE tid=%s", tid)
    if not topic :
        raise HZActionError('No such topic')
    if not topic.oldfilename :
        logger.warning("Try delete a no oldfilename file, userid=%s, fromhost=%s, topic=%s", userid, request.remote_addr, topic)
        return True
    r = getclient().do_del(board=topic.boardname,
                           file=topic.oldfilename)
    if 'error' in r :
        if r['emsg'] == u"文件不存在, 删除失败" :
            if(isowner_topic(userid, tid)):
                logger.warning("Delete a no exists file, filename=%s, userid=%, fromhost=%s, topic=%s", topic.oldfilename, authed, request.remote_addr, topic)
                return True
        raise HZActionError(r['emsg'])
    return True

@delreply.guard
def del_fs_reply(userid, rid, **ps) :
    db = getconn()
    reply = db.get(u"SELECT tid, oldfilename FROM herzog_reply"
                   "  WHERE rid=%s", rid)
    if not reply :
        raise HZActionError('No such reply')
    if not reply.oldfilename :
        logger.warning("Try delete a no oldfilename file, userid=%s, fromhost=%s, reply=%s", userid, request.remote_addr, reply)
        return True
    topic = db.get(u"SELECT boardname FROM herzog_topic"
                   "  WHERE tid=%s", reply.tid)
    if not topic :
        raise HZActionError('No such topic')
    r = getclient().do_del(board=topic.boardname,
                           file=reply.oldfilename)
    if 'error' in r :
        if r['emsg'] == u"文件不存在, 删除失败" :
            if(isowner_topic(userid, tid)):
                warning("Delete a no exists file, filename=%s, userid=% [%s], fromhost=%s", topic.oldfilename, authed, request.remote_addr, topic)
                return True
        raise HZActionError(r['emsg'])
    return True


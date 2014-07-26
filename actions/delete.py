from herzog.base import action, getconn
from herzog.base.action import priority

@action
def deltopic(userid, tid, **ps):
    db.execute(u"DELETE FROM herzog_topic"
               "  WHERE tid=%s", tid)
    return dict(ret=True)

@action
def delreply(userid, rid, **ps):
    db.execute(u"DELETE FROM herzog_reply"
               "  WHERE rid=%s", rid)
    return dict(ret=True)

@deltopic.guard
def isowner_topic(userid, tid, **ps) :
    return db.get(u"SELECT tid FROM herzog_topic"
                  " WHERE tid=%s AND owner=%s",
                  tid, userid) is not None

@delreply.guard
def isowner_reply(userid, rid, **ps) :
    return db.get(u"SELECT rid FROM herzog_reply"
                  " WHERE rid=%s AND owner=%s",
                  rid, userid) is not None


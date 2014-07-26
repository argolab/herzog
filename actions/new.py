from herzog.base import action, getconn, HZActionError, flag
from herzog.base.misc import dt, gen_summary

@action
def topic(userid, boardname, title, content, fromaddr, time=None,
          summary=None, fromapp='', **ps) :
    if time is None :
        time = dt.now()
    if summary is None :
        summary = gen_summary(content)
    if title > 36 :
        title = title[:36]
    tid = getconn().execute(
        u" INSERT INTO herzog_topic"
        "   (boardname, owner, title, lastupdate, lastreply,"
        "    lastcomment, fromaddr, summary, content)"
        "  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        boardname, userid, title, time, time, time, fromaddr,
        summary, content)
    return dict(tid=tid)

@action
def reply(userid, tid, content, fromaddr, time=None,
          summary=None, fromapp='', *ps) :
    replyid = brid = 0
    if time is None :
        time = dt.now()

    db = getconn()
    rid = db.execute(u"INSERT INTO herzog_reply"
                     "  (tid, brid, replyid, owner, lastupdate,"
                     "   fromaddr, fromapp, content) VALUES"
                     " (%s, %s, %s, %s, %s, %s, %s, %s)",
                     tid, brid, replyid, userid, time, fromaddr,
                     fromapp, content)
    db.execute(u"UPDATE herzog_reply SET brid=%s WHERE rid=%s",
               rid, rid)
    db.execute(u"UPDATE herzog_topic SET lastreply=%s WHERE tid=%s",
               time, tid)

    return dict(rid=rid)

@action
def comment(userid, replyid, content, fromaddr, time=None,
            summary=None, fromapp='', *ps) :
    if time is None :
        time = dt.now()

    db = getconn()

    reply = db.get("SELECT tid, brid FROM herzog_reply WHERE rid=%s", replyid)
    if not reply :
        raise HZActionError("No such topic")

    rid = db.execute(u"INSERT INTO herzog_reply"
                     "  (tid, brid, replyid, owner, lastupdate,"
                     "   fromaddr, content) VALUES"
                     " (%s, %s, %s, %s, %s, %s, %s)",
                     reply.tid, reply.brid, replyid, userid, time,
                     fromaddr, content)
    db.execute(u"UPDATE herzog_topic SET lastcomment=%s WHERE tid=%s",
               time, reply.tid)

    return dict(rid=rid, tid=reply.tid)

@reply.guard
def reply_topic_exists(tid, **ps) :
    topic = getconn().get(u"SELECT tid FROM herzog_topic WHERE tid=%s", tid)
    if not topic :
        raise HZActionError("No such topic")
    return True

@comment.guard
def comment_reply_exists(replyid, **ps) :
    reply = getconn().get(u"SELECT rid FROM herzog_reply WHERE rid=%s",
                          replyid)
    if not reply :
        raise HZActionError("No such reply")
    return True

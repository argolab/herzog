from herzog.base import action, getconn
from herzog.base.misc import dt, gen_summary

@action
def topic(userid, boardname, title, content, fromaddr, time=None,
          summary=None, fromapp='', **ps) :
    if time is None :
        time = dt.now()
    if summary is None :
        summary = gen_summary(content)
    tid = db.execute(
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

    rid = db.execute(u"INSERT INTO herzog_reply"
                     "  (tid, brid, replyid, owner, lastupdate,"
                     "   fromaddr, content) VALUES"
                     " (%s, %s, %s, %s, %s, %s, %s)",
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
    reply = db.get("SELECT tid, brid FROM herzog_reply WHERE rid=%s", replyid)
    if time is None :
        time = dt.now()

    rid = db.execute(u"INSERT INTO herzog_reply"
                     "  (tid, brid, replyid, owner, lastupdate,"
                     "   fromaddr, content) VALUES"
                     " (%s, %s, %s, %s, %s, %s, %s)",
                     reply.tid, reply.brid, replyid, userid, time,
                     fromaddr, content)
    db.execute(u"UPDATE herzog_topic SET lastcomment=%s WHERE tid=%s",
               time, tid)

    return dict(rid=rid)


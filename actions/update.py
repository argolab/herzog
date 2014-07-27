from herzog.base import action, getconn, HZActionError, flag, authed
from herzog.base.misc import getnow, gen_summary

@action
def update_topic(userid, tid, title, content, **ps):
    db = getconn()
    now = getnow()
    summary = gen_summary(content)
    db.execute(u"UPDATE herzog_topic SET title=%s, content=%s, lastupdate=%s,"
               "  summary=%s WHERE tid=%s", title, content, now, summary, tid)
    return dict()

@action
def update_reply(userid, rid, content, **ps):
    db = getconn()
    now = getnow()
    db.execute(u"UPDATE herzog_reply SET content=%s, lastupdate=%s"
               "  WHERE rid=%s", content, now, rid)
    return dict()

from herzog.base import action, getconn, HZActionError, flag, abort
from herzog.base.misc import getnow, issysop
from herzog.base.log import getlogger
from herzog.actions.new import (
    topic as a_topic,
    reply as a_reply,
    comment as a_comment
)

logger = getlogger(__name__)

def flagup(userid, flag, tid=None, rid=None) :
    db = getconn()
    if tid :
        dt = db.get(u"SELECT utid FROM herzog_topicship"
                    "  WHERE userid=%s AND tid=%s", userid, tid)
        if dt :
            dt = dt.utid
            db.execute(u"UPDATE herzog_topicship SET flag=flag|%s"
                       "  WHERE utid=%s", flag, dt)
        else :
            dt = db.insert(u"INSERT INTO herzog_topicship"
                           "  (userid, tid, flag) VALUES"
                           " (%s, %s, %s)", userid, tid, flag)
    else :
        dt = db.get(u"SELECT utid FROM herzog_replyship"
                    "  WHERE userid=%s AND rid=%s", userid, rid)
        if dt :
            dt = dt.utid
            db.execute(u"UPDATE herzog_replyship SET flag=flag|%s"
                       "  WHERE utid=%s", flag, dt)
        else :
            dt = db.insert(u"INSERT INTO herzog_replyship"
                           "  (userid, rid, flag) VALUES"
                           " (%s, %s, %s)", userid, rid, flag)
    return dt

def flagdown(userid, flag, tid=None, rid=None) :
    db = getconn()
    if tid :
        dt = db.get(u"SELECT utid FROM herzog_topicship"
                    "  WHERE userid=%s AND tid=%s AND (flag & %s >0)",
                    userid, tid, flag)
        if dt is None :
            return False
        dt = dt.utid
        db.execute(u"UPDATE herzog_topicship SET flag=flag^%s"
                   " WHERE utid=%s", flag, dt)
    else :
        dt = db.get(u"SELECT utid FROM herzog_replyship"
                    "  WHERE userid=%s AND rid=%s AND (flag & %s >0)",
                    userid, rid, flag)
        if not dt :
            return False
        dt = dt.utid
        db.execute(u"UPDATE herzog_replyship SET flag=flag^%s"
                   " WHERE utid=%s", flag, dt)
    return dt
    
@action
def upvote(userid, tid=None, rid=None, **ps):
    db = getconn()
    if tid :
        db.execute(u"UPDATE herzog_topic SET upvote=upvote+1"
                   " WHERE tid=%s", tid)
        dt = flagup(userid, flag.UPVOTE, tid=tid)
    else :
        db.execute(u"UPDATE herzog_reply SET upvote=upvote+1"
                   " WHERE rid=%s", rid)
        dt = flagup(userid, flag.UPVOTE, rid=rid)
    return dict(dt=dt)

@action
def unvote(userid, tid=None, rid=None, **ps):
    if flagdown(userid, flag.UPVOTE, tid=tid, rid=rid) is False :
        raise HZActionError("Have not vote it")
    db = getconn()
    if tid :
        db.execute(u"UPDATE herzog_topic SET upvote=upvote-1"
                   " WHERE tid=%s", tid)
    else :
        db.execute(u"UPDATE herzog_reply SET upvote=upvote-1"
                   " WHERE rid=%s", rid)
    return dict()        

@upvote.guard
def norepeatvote(userid, tid=None, rid=None, **ps):
    if tid :
        if getconn().get(
                u"SELECT tid FROM herzog_topicship"
                " WHERE userid=%s AND tid=%s AND (flag & %s >0)",
                userid, tid, flag.UPVOTE) :
            raise HZActionError("No vote again")
    else :
        if getconn().get(
                u"SELECT rid FROM herzog_replyship"
                " WHERE userid=%s AND rid=%s AND (flag & %s >0)",
                userid, rid, flag.UPVOTE) :
            raise HZActionError('No vote again')
    return True
        
@action
def star(userid, tid=None, rid=None, **ps):
    if tid is not None :
        dt = flagup(userid, flag.STAR, tid=tid)
    else :
        dt = flagup(userid, flag.STAR, rid=rid)
    return dict(dt=dt)

@action
def unstar(userid, tid=None, rid=None, **ps):
    if flagdown(userid, flag.STAR, tid=tid, rid=rid) is False :
        raise HZActionError("Have not star it")
    return dict()

@action
def setv(userid, tid, v, **ps):
    db = getconn()
    db.execute(u"UPDATE herzog_topic SET v=%s WHERE tid=%s", v, tid)
    return dict()

@setv.guard
def g_issysop(userid, *args, **ps):
    if not issysop(userid) :
        logger.warning("Try to setv userid=%s", userid)
        abort(404)
    return True

@a_topic.after
def flag_newtopic(ret, userid, **ps):
    flagup(userid, flag.OWNER, tid=ret['tid'])

@a_reply.after
def flag_reply(ret, userid, tid, **ps):
    db = getconn()
    now = getnow()
    if db.get(u"SELECT utid FROM herzog_topicship"
              "   WHERE userid=%s AND tid=%s AND (flag & %s >0)",
              userid, tid, flag.SPEAK) :
        db.execute(u"UPDATE herzog_topic SET replynum=replynum+1"
                   "  , lastreply=%s WHERE tid=%s", tid, now)
    else :
        db.execute(u"UPDATE herzog_topic SET replynum=replynum+1"
                   "  , partnum=partnum+1, lastreply=%s WHERE tid=%s",
                   tid, now)
    flagup(userid, flag.REPLY, tid=tid)

@a_comment.after
def flag_comment(ret, userid, replyid, **ps):
    db = getconn()
    now = getnow()
    if db.get(u"SELECT utid FROM herzog_topicship"
              "  WHERE userid=%s AND tid=%s AND (flag & %s >0)",
              userid, ret['tid'], flag.SPEAK) :
        db.execute(u"UPDATE herzog_topic SET lastcomment=%s"
                   "  WHERE tid=%s", now, ret['tid'])
    else :
        db.execute(u"UPDATE herzog_topic SET partnum=partnum+1"
                   " , lastreply=%s WHERE tid=%s", now, ret['tid'])
    flagup(userid, flag.COMMENT, tid=ret['tid'])
    flagup(userid, flag.COMMENT, rid=replyid)


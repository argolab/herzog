#-*- coding: utf-8 -*-

from herzog.base import app, getclient, jsonify, render_template, request, ajax_fields_error, authed, redirect, getconn, json_success, getbbsfile, getfields
from herzog.base.misc import getnow, filter_ansi, quote_title
from herzog.actions.new import topic, reply, comment
from herzog.actions.postship import upvote
from codecs import open
import re

TYPE_REPLY = 1
TYPE_AT = 2
TYPE_UPVOTE = 3

RE_AT = re.compile(r'(?:^| )@(\w{2,20})')

@reply.after
def send_reply_notification(ret, userid, tid, *args, **kwargs) :
    db = getconn()
    touserid = db.get(u"SELECT userid, title FROM herzog_topic"
                      "  WHERE tid=%s", tid)
    params = '%s\n%s\n%s\n%s' % (touserid.title.replace('\n', ' '),
                                 authed(), tid, ret['rid'])
    now = getnow()
    db.execute(u"INSERT INTO herzog_notification"
               "  (userid, t, params, s, lastupdate)"
               " VALUES (%s, %s, %s, %s, %s)",
               touserid.userid, TYPE_REPLY, params, tid, now)
    
@topic.after
@reply.after
@comment.after
def send_at_notification(ret, *args, **kwargs) :
    db = getconn()
    if 'tid' in ret :
        tid = ret['tid']
        title = kwargs['title']
        rid = 0
    else :
        tid = kwargs['tid']
        rid = ret['rid']
        title = db.get(u"SELECT title FROM herzog_topic"
                       "  WHERE tid=%s", tid)
        title = title['title']
    params = '%s\n%s\n%s\n%s' % (title.replace('\n', ' '),
                                 authed(), tid, rid)
    touserids = RE_AT.findall(kwargs['content'])[:5]
    cli = getclient()
    now = getnow()
    for touserid in touserids :
        userid = cli.userexists(userid=touserid)
        if 'userid' in userid :
            userid = userid['userid']
        else :
            continue
        db.execute(u"INSERT INTO herzog_notification"
                   "  (userid, t, params, s, lastupdate)"
                   " VALUES (%s, %s, %s, %s, now)",
                   touserid, TYPE_AT, params, tid, now)

@upvote.after
def send_upvote_notification(ret, userid, tid=None, rid=None, *args, **kwargs) :
    db = getconn()
    if 'tid' is not None :
        rid = 0
        title = db.get(u"SELECT title, owner FROM herzog_topic"
                       "  WHERE tid=%s", tid)
        touserid = title['owner']
        title = title['title']
    else :
        tid = db.get(u"SELECT tid FROM herzog_reply"
                     "  WHERE rid=%s", rid)
        tid = tid['tid']
        title = db.get(u"SELECT title, owner FROM herzog_topic"
                       "  WHERE tid=%s", tid)
        touserid = title['owner']
        title = title['title']
    params = '%s\n%s\n%s\n%s' % (title.replace('\n', ' '),
                                 authed(), tid, rid)
    cli = getclient()
    touserid = cli.userexists(userid=touserid)
    now = getnow()
    if 'userid' in touserid :
        touserid = touserid['userid']
        db.execute(u"INSERT INTO herzog_notification"
                   "  (userid, t, params, s, lastupdate)"
                   " VALUES (%s, %s, %s, %s, %s)",
                   touserid, TYPE_UPVOTE, params, tid, now)

@app.route('/notification/')
def notification():
    try :
        offset = int(request.args.get('offset', 0))
    except:
        offset = 0    
    userid = authed()
    db = getconn()
    notification = db.query(u"SELECT nid,t,params,lastupdate"
                      " FROM herzog_notification"
                      " WHERE userid=%%s"
                      " ORDER BY lastupdate DESC"
                      " LIMIT %d, 15" % offset, userid)

    # update touch
    touch = db.get(u"SELECT touch_notification"
                   " FROM herzog_userdata"
                   " WHERE userid=%s", userid)
    now = getnow()
    if touch :
        touch = touch.touch_notification
        db.execute(u"UPDATE herzog_userdata SET "
                   "  touch_notification=%s"
                   "  WHERE userid=%s", now, userid)
    else :
        db.execute(u"INSERT INTO herzog_userdata "
                   "  (userid, touch_notification, touch_starpost)"
                   " VALUES (%s, %s, %s)",
                   userid, now, now)
    
    return json_success(notification=notification, touch=touch)

@app.route('/starpost')
def starpost():
    userid = authed()
    db = getconn()
    starpost = db.query(u"SELECT herzog_topic.tid,title"
                        " FROM herzog_topic INNER JOIN herzog_topicship"
                        " ON herzog_topic.tid = herzog_topicship.tid"
                        " WHERE herzog_topicship.userid=%s AND"
                        "   herzog_topicship.flag & 8"
                        " ORDER BY herzog_topic.lastreply DESC"
                        " LIMIT 15", userid)

    # update touch time
    touch = db.get(u"SELECT touch_starpost FROM herzog_userdata"
                   " WHERE userid=%s", userid)
    now = getnow()
    if touch :
        touch = touch.touch_starpost
        db.execute(u"UPDATE herzog_userdata SET touch_starpost=%s"
                    "  WHERE userid=%s", now, userid)
    else :
        db.execute(u"INSERT INTO herzog_userdata "
                   "  (userid, touch_notification, touch_starpost)"
                   " VALUES (%s, %s, %s)", userid, now, now)

    return json_success(starpost=starpost, touch=touch)

@app.route('/ajax/message')
def message():
    userid = authed()
    message = getclient().getmessage()
    db = getconn()
    touch = db.get(u"SELECT touch_notification,touch_starpost"
                   " FROM herzog_userdata"
                   " WHERE userid=%s", userid)
    if touch :
        touch_notification = touch.touch_notification
        touch_starpost = touch.touch_starpost
    else :
        touch_notification = touch_starpost = 0
    notification_num = getconn().get(u"SELECT count(nid) as t FROM herzog_notification"
                                 " WHERE userid=%s AND (lastupdate > %s)"
                                 " ORDER BY lastupdate DESC"
                                 " LIMIT 6", userid, touch_notification)
    print notification_num, touch_notification
    star_num = getconn().get(u"SELECT count(herzog_topic.tid) as t FROM herzog_topic"
                               "  INNER JOIN herzog_topicship"
                               " ON herzog_topic.tid = herzog_topicship.tid"
                               " WHERE herzog_topicship.userid=%s AND"
                               "   herzog_topicship.flag & 8"
                               "   AND herzog_topic.lastreply > %s"
                               " LIMIT 15", userid, touch_starpost)
    return '%s,%s,%s,%s' % (message['newfavs'], message['mails'],
                            notification_num['t'], star_num['t'])

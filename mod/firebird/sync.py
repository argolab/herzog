from herzog.base import app, request, g, getconn
from herzog.base.misc import getfspost
from herzog.base.log import getlogger
from herzog.actions.new import (
    topic as topic0,
    reply as reply0,
    comment as comment0
)
from herzog.mod.notification import (
    send_reply_notification,
    send_at_notification,
)
from herzog.actions.delete import (
    deltopic as deltopic0,
    delreply as delreply0
)
from herzog.actions.update import (
    update_topic as update_topic0,
    update_reply as update_reply0
)
from herzog.actions.postship import (
    flag_newtopic, flag_reply, flag_comment
)
from herzog.mod.firebird.new import (
    update_filename_topic, update_filename_reply
)

logger = getlogger(__name__)

topic = topic0.prototype()
topic.after(flag_newtopic)
topic.after(update_filename_topic)
topic.after(send_at_notification)

reply = reply0.prototype()
reply.after(flag_reply)
reply.after(update_filename_reply)
reply.after(send_reply_notification)
reply.after(send_at_notification)

comment = comment0.prototype()
comment.after(flag_comment)
comment.after(update_filename_reply)
comment.after(send_at_notification)

deltopic = deltopic0.prototype()
delreply = delreply0.prototype()

update_topic = update_topic0.prototype()
update_reply = update_reply0.prototype()

def syncor(f):
    def inner():
        # try:
            # f(**request.args)
        # except :
            # logger.error('[%s] : %s', request.method, request.path)
        f(**dict(request.form.items()))
        return '1'
    inner.func_name = f.func_name
    return inner

def query_postid(b, f) :
    db = getconn()
    topic = db.get(u"SELECT tid FROM herzog_topic"
                   "  WHERE boardname=%s AND oldfilename=%s LIMIT 1",
                   b, f)
    if topic :
        return topic
    reply = db.get(u"SELECT rid FROM herzog_reply LEFT JOIN herzog_topic"
                   "  ON herzog_reply.tid = herzog_topic.tid"
                   "  WHERE herzog_reply.oldfilename=%s AND boardname=%s LIMIT 1",
                   f, b)
    if reply :
        return reply
    return None

@app.route("/_hfb/post/newtopic", methods=["POST"])
@syncor
def sync_newtopic(b, f, h):
    a, c, q, t = getfspost(b, f)
    g._filename = f
    topic(userid=a['owner'], boardname=b,
          title=a['title'].decode('gbk', 'ignore'),
          content=c.decode('gbk', 'ignore'), fromaddr=h)

@app.route("/_hfb/post/reply", methods=["POST"])
@syncor
def sync_reply(b, f, f0, h):
    a, c, q, t = getfspost(b, f)
    post = query_postid(b, f0)
    g._filename = f
    if not post :
        logger.error('Sync reply noexists: boardname=%s filename=%s [%s]',
                     b, f0, h)
        return
    elif post.has_key('tid') :
        reply(userid=a['owner'], tid=post.tid, content=c.decode('gbk', 'ignore'), fromaddr=h)
    elif post.has_key('rid') :
        comment(userid=a['owner'], replyid=post.rid, content=c.decode('gbk', 'ignore'), fromaddr=h)

@app.route("/_hfb/post/cross", methods=["POST"])
@syncor
def async_cross(b, f, h):
    a, c, q, t = getfspost(b, f)
    g._filename = f
    topic(a['owner'], b, a['title'].decode('gbk', 'ignore'),
          c.decode('gbk', 'ignore'), h)

@app.route("/_hfb/post/updatepost", methods=["POST"])
@syncor
def sync_updatepost(b, f, h):
    a, c, q, t = getfspost(b, f)
    post = query_postid(b, f)
    if not post :
        logger.error('Sync update noexists: boardname=%s filename=%s [%s]',
                     b, f, h)
        return
    elif post.has_key('tid') :
        update_topic(a['owner'], post.tid,
                     a['title'].decode('gbk', 'ignore'),
                     c.decode('gbk', 'ignore'))
    elif post.has_key('rid') :
        update_reply(a['owner'], reply.rid, c.decode('gbk', 'ignore'))

@app.route("/_hfb/post/del", methods=["POST"])
@syncor
def sync_delete(b, f, h):
    a, c, q, t = getfspost(b, f)
    post = query_postid(b, f)
    if not post :
        logger.error('Sync delete noexists: boardname=%s filename=%s [%s]',
                     b, f, h)
        return
    elif post.has_key('tid') :
        deltopic(a['owner'], post.tid)
    elif post.has_key('rid') :
        delreply(a['owner'], post.rid)

from herzog.base import app, render_template, getconn, abort, getfields, ajax_fields_error, request, json_success, escape
from herzog.base.template_helper import postHtml, url_for_avatar

@app.route('/t/<int:tid>')
def topic(tid):
    db = getconn()
    topic = db.get(u"SELECT tid, owner, title, score, v, lastupdate,"
                   "   lastreply, replynum, partnum, upvote, fromapp,"
                   "   flag, content FROM herzog_topic WHERE tid=%s", tid)
    if not topic :
        abort(404)
    replys0 = db.query(u"SELECT rid, brid, replyid, owner, lastupdate,"
                       "  fromapp, flag, content FROM herzog_reply"
                       "  WHERE tid=%s ORDER BY brid LIMIT 100", tid)
    lastbranch = None
    lastcomments = None
    replys = []
    for r in replys0 :
        if lastbranch is None or r.brid != lastbranch.brid :
            lastcomments = r['comments'] = []
            lastbranch = r
            replys.append(r)
        else :
            lastcomments.append(r)

        
    return render_template('topic.html', topic=topic, replys=replys)

@app.route('/ajax/reply')
@ajax_fields_error
def ajax_get_reply():
    form = getfields(_require=('rid',), _form=request.args)
    db = getconn()
    reply = db.get(u"SELECT rid, brid, replyid, owner, lastupdate,"
                   "  fromapp, flag, content FROM herzog_reply"
                   "  WHERE rid=%s", form['rid'])
    reply['html_content'] = postHtml(reply['content'])
    reply['owner_avatar'] = url_for_avatar(reply['owner'])
    return json_success(reply=reply)

from herzog.base import app, render_template, getconn, abort

@app.route('/t/<int:tid>')
def topic(tid):
    db = getconn()
    topic = db.get(u"SELECT tid, owner, title, score, v, lastupdate,"
                   "   lastreply, replynum, partnum, upvote, fromapp,"
                   "   flag, content FROM herzog_topic WHERE tid=%s", tid)
    if not topic :
        abort(404)
    replys = db.query(u"SELECT rid, brid, replyid, owner, lastupdate,"
                      "  fromapp, flag, content FROM herzog_reply"
                      "  WHERE tid=%s ORDER BY brid LIMIT 100", tid)
    return render_template('topic.html', topic=topic, replys=replys)

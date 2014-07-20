from app import (
    app, render_template, _j, flag, request,
    flag, getuserid, getconn, getnow, trigger, jsonify,
    parse_int, Precondition
)

@app.route('/')
def fresh():
    fresh = _j('fresh')
    topten = _j('topten')
    return render_template('fresh.html', fresh=fresh,
                           topten=topten)

@app.route('/b/<boardname>')
def board(boardname):
    return render_template('board.html', **_j('board'))

@app.route('/t/<int:tid>')
def topic(tid):
    return render_template('topic.html',
                           **_j('topic'))

@app.route('/ajax/post/fresh')
def ajax_fresh():
    return

@app.route('/ajax/post/read')
def ajax_read():
    return

@app.route('/ajax/post/list')
def ajax_listpost():
    boardname = request.args.get('boardname')
    limit = parse_int(request.args.get('limit'), 1, 40, 20)
    cursor = request.args.get('cursor')
    db = getconn()
    if not boardname :
        return jsonify(error=1, msg="Need param boardname")
    if cursor :
        if cursor :
            try :
                cursor = float(cursor)
            except ValueError :
                return jsonify(error=1, msg="Wrong cursor value")
        posts = db.query(u" SELECT tid, owner, title, posttime, score,"
                         "    lastreply, replynum, partnum, upvote,"
                         "    summary, flag"
                         " FROM herzog_topic"
                         " WHERE boardname=%s AND score<%s"
                         "   ORDER BY score DESC LIMIT %s",
                         boardname, cursor, limit)
    else :
        posts = db.query(u" SELECT tid, owner, title, posttime, score,"
                         "    lastreply, replynum, partnum, upvote,"
                         "    summary, flag"
                         " FROM herzog_topic"
                         " WHERE boardname=%s ORDER BY score DESC LIMIT %s",
                         boardname, limit)
    if posts :
        nextcursor = posts[-1]['score']
    else :
        nextcursor = None
    return jsonify(success=1, posts=posts, nextcursor=nextcursor)

@app.route('/ajax/post/new', methods=["POST"])
def ajax_newpost():
    boardname = request.form.get('boardname')
    title = request.form.get('title')
    userid = getuserid()
    fromaddr = request.remote_addr
    content = request.form.get('content')
    summary =  request.form.get('summary') or gen_summary(content)

    if not(boardname and title and userid and fromaddr and content and \
           summary) :
        return jsonify(error=1, emsg="All param need boardname, title, "
                       "userid, fromaddr, content, summary")

    data = dict(boardname=boardname, title=title, userid=userid,
                fromaddr=fromaddr, content=content, summary=summary)

    try:
        trigger('require_newtopic', **data)
    except Precondition as e :
        return jsonify(error=1, emsg=e.kwargs['message'])

    db = getconn()
    now = getnow()
    tid = db.execute(u" INSERT INTO herzog_topic"
                     "   (boardname, owner, title, posttime, lastreply,"
                     "    lastcomment, fromaddr, summary, content)"
                     "  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     boardname, userid, title, now, now, now, fromaddr,
                     summary, content)
    utid = db.execute(u" INSERT INTO herzog_postship"
                      " (userid, tid, flag) VALUES"
                      " (%s, %s, %s)", userid, tid, flag.NEWPOST)

    data['tid'] = tid
    data['utid'] = utid
    
    trigger("success_newtopic", **data)
    return jsonify(success=1, msg="success post",
                   tid=tid, utid=utid)

@app.route('/ajax/post/reply')
def ajax_replypost():
    return

@app.route('/ajax/post/mark')
def ajax_markpost():
    return

@app.route('/ajax/post/del')
def ajax_delpost():
    return

@app.route('/ajax/post/up')
def ajax_uppost():
    return

@app.route('/ajax/post/star')
def ajax_starpost():
    return

@app.route('/ajax/post/report')
def ajax_reportpost():
    return

@app.route('/ajax/post/_addpoint')
def ajax_addpointpost():
    return

@app.route('/ajax/post/_recommend')
def ajax_recommendpost():
    return

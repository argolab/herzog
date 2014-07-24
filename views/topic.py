#/usr/bin/python

from app import (
    app, render_template, _j, flag, request,
    flag, getuserid, getconn, getnow, trigger, jsonify,
    parse_range, Precondition, is_sysop, parse_int,
    abort, getclient
)

# need check user login

@app.route('/')
def fresh():
    db = getconn()
    topics = db.query(u"SELECT tid, owner, title, score, v, lastupdate,"
                      "   lastreply, replynum, partnum, upvote, fromapp,"
                      "   flag, content, boardname FROM herzog_topic"
                      "  ORDER BY score DESC LIMIT 20")
    # TODO : topics may be NONE
    # TODO : perm filter
    # TODO : fresh and topten
    fresh = _j('fresh')
    topten = _j('topten')
    return render_template('fresh.html', fresh=fresh,
                           topten=topten)

@app.route('/b/<boardname>')
def board(boardname):
    db = getconn()
    board = getclient().showboard(board=boardname)
    if 'error' in board :
        # return error for user
        abort(404)
    topics = db.query(u"SELECT tid, owner, title, score, v, lastupdate,"
                      "   lastreply, replynum, partnum, upvote, fromapp,"
                      "   flag, content FROM herzog_topic WHERE boardname=%s"
                      "  ORDER BY score DESC LIMIT 20", boardname)
    
    return render_template('board.html', board=board, topics=topics)

@app.route('/t/<int:tid>')
def topic(tid):
    db = getconn()
    topic = db.get(u"SELECT tid, owner, title, score, v, lastupdate,"
                   "   lastreply, replynum, partnum, upvote, fromapp,"
                   "   flag, content FROM herzog_topic WHERE tid=%s", tid)
    if not topic :
        abort(404)
    replys = db.query(u"SELECT rid, brid, replyid, owner, lastupdate,"
                      "  fromapp, flag, content FROM herzog_topic"
                      "  WHERE tid=%s ORDER BY brid LIMIT 100", tid)
    return render_template('topic.html', topic=topic, replys=replys)

@app.route('/ajax/post/fresh')
def ajax_fresh():
    cursor = request.args.get('cursor')
    topics = db.query(u"SELECT tid, owner, title, score, v, lastupdate,"
                      "   lastreply, replynum, partnum, upvote, fromapp,"
                      "   flag, content WHERE score < %s"
                      "   ORDER BY score DESC LIMIT 20", cursor)
    return jsonify(topics=topics)

@app.route('/ajax/post/read')
def ajax_read():
    tid = request.args.get('tid')
    cursor = request.args.get('cursor')
    limit = parse_range(request.args.get("limit"), 20, 0, 40)
    db = getconn()
    if cursor :
        cursor = parse_range(cursor, 20, 0, 40)
        replys = db.query(u"SELECT rid, brid, replyid, owner, lastupdate,"
                          "   fromaddr, fromapp, flag, content"
                          "  WEHER tid=%s AND rid<%s LIMIT %s",
                          tid, cursor, limit)
    else :
        replys = db.query(u"SELECT rid, brid, replyid, owner, lastupdate,"
                          "   fromaddr, fromapp, flag, content"
                          "  WEHER tid=%s LIMIT %s",
                          tid, limit)
    return jsonify(success=1, replys=replys)

@app.route('/ajax/post/list')
def ajax_listpost():
    boardname = request.args.get('boardname')
    limit = parse_range(request.args.get('limit'), 1, 40, 20)
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
        posts = db.query(u" SELECT tid, owner, title, lastupdate, score,"
                         "    lastreply, replynum, partnum, upvote,"
                         "    summary, flag"
                         " FROM herzog_topic"
                         " WHERE boardname=%s AND score<%s"
                         "   ORDER BY score DESC LIMIT %s",
                         boardname, cursor, limit)
    else :
        posts = db.query(u" SELECT tid, owner, title, lastupdate, score,"
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
    try:
        form = valid(request.form,
                     _require=('boardname', 'title', 'content'),
                     _optional=('summary'))
        userid = getuserid()
        if 'summary' not in form:
            form.summary = gen_summary(form['content'])
        form.userid = userid
        form.fromaddr = request.remote_addr
        
        trigger('require_newtopic', **data)
        
        db = getconn()
        now = getnow()
        tid = db.execute(
            u" INSERT INTO herzog_topic"
            "   (boardname, owner, title, lastupdate, lastreply,"
            "    lastcomment, fromaddr, summary, content)"
            "  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            boardname, userid, title, now, now, now, fromaddr,
            summary, content)

        trigger('success_newtopic', tid=tid, userid=request.remote_addr)
        
        return json_success(tid=tid, utid=utid)
        
    except (ValidError, AuthError, Precondition) as e:
        return json_error(e)

def gettopic(tid) :
    key = "topic%d" % tid
    if hasattr(g, key) :
        return getattr(g, key)
    db = getconn()
    ret = db.get(u"SELECT rid, tid, brid, replyid, owner,"
                 "   lastupdate, fromaddr, fromapp, flag,"
                 "   oldfilename FROM herzog_topic WHERE tid=%s",
                 tid)
    setattr(g, key, ret)
    return ret

def getreply(rid) :
    key = "reply%d" % rid
    if hasattr(g, key) :
        return getattr(g, key)
    db = getconn()
    ret = db.get(u"SELECT rid, tid, brid, replyid, owner,"
                 "   lastupdate, fromaddr, fromapp, flag,"
                 "   oldfilename FROM herzog_reply WHERE rid=%s",
                 rid) or None
    setattr(g, key, ret)
    return ret    

def v_topic(tid):
    if gettopic(tid) is None :
        raise ValidError("No such topic", tid=tid)
    return tid

def v_reply(rid):
    if getreply(rid) is None :
        raise ValidError('No such reply', rid=rid)
    return rid

@app.route('/ajax/post/reply', methods=["POST"])
def ajax_replypost():
    try:
        userid = getuserid()
        form = valid(request.form, _require=("content",),
                     _optional=('tid', 'replyid'),
                     tid=v_topic, replyid=v_reply)
        if not form.tid and not form.replyid :
            raise ValidError('Need tid or replyid')

        if form.tid is not None :
            form.replyid = form.brid = 0
        else :
            reply = getreply(form.replyid)
            form.tid = v_topic(reply.tid)
            form.brid = reply.brid

        trigger('require_reply', userid=userid,
                fromaddr=request.remote_addr, **form)

        # insert content
        now = getnow()
        db = getconn()
        irid = db.execute(u"INSERT INTO herzog_reply"
                          "  (tid, brid, replyid, owner, lastupdate,"
                          "   fromaddr, content) VALUES"
                          " (%s, %s, %s, %s, %s, %s, %s)",
                          form.tid, form.brid, form.replyid,
                          form.userid, now, form.fromaddr, form.content)
        if brid == 0 :
            db.execute(u"UPDATE herzog_reply SET brid=%s WHERE rid=%s",
                       form.rid, form.rid)

        trigger('success_reply', rid=rid, replyid=replyid, userid=userid)
        return json_success(rid=rid)
    except (ValidError, AuthError, Precondition) as e:
        return json_error(e)


# just delete if hv success
@app.route('/ajax/post/del')
def ajax_delpost():
    if request.form.get('tid') :
        tid = parse_int(request.form.get('tid'))
        if tid is None :
            return jsonify(error=1, msg="Wrong tid")
        ret = db.get(u"SELECT boardname, tid, oldfilename"
                     "  WHERE tid=%s", tid)
        if not ret :
            return jsonify(error=1, msg="Wrong tid")
        r = getclient().do_del(board=ret.boardname,
                               file=ret.oldfilename)
        if 'success' in r :
            db.execute(u"DELETE FROM herzog_topic"
                       "  WHERE tid=%s", ret.tid)
            return jsonify(success=1, msg="delete success")
        return jsonify(error=1, msg=r.emsg)
    else :
        rid = parse_int(request.form.get('rid'))
        if rid is None :
            return jsonify(error=1, msg="Wrong rid")
        ret = db.get(u"SELECT tid, oldfilename WHERE rid=%s", rid)
        if not ret :
            return jsonify(error=1, msg="Wrong rid")
        topic = db.get(u"SELECT boardname WHERE tid=%s", ret.tid)
        r = getclient().do_del(board=topic.boardname,
                               file=ret.oldfilename)
        if 'success' in r :
            db.execute(u"DELETE FROM herzog_reply"
                       "  WHERE rid=%s", rid)
            return jsonify(success=1, msg="delete reply success")
        return jsonify(error=1, msg=r.emsg)

def try_set_flag(tid, flag_type):
    try :
        tid = int(tid)
    except (ValueError, TypeError) :
        return dict(error=1, msg="Wrong tid")
    db = getconn()
    userid = getuserid()
    if not db.get(u"SELECT tid FROM herzog_topic WHERE tid=%s", tid):
        return dict(error=1, msg="Wrong tid")
    utid = db.get(u"SELECT utid, flag FROM herzog_topicship"
                  "  WHERE userid=%s AND tid=%s", userid, tid)
    if not utid :
        utid = db.execute(u"INSERT INTO herzog_topicship"
                          "   (userid, tid, flag) VALUES"
                          "  (%s, %s, %s)", userid, tid, flag_type)
    else :
        if utid.flag & flag_type > 0 :
            return dict(error=1, msg="Started")
        utid.flag = utid.flag | flag_type
        db.execute(u"UPDATE herzog_topic SET flag=%s"
                   "  WHERE utid=%s", utid.flag, utid.utid)
    return dict(success=1, msg="Stat success", utid=utid)

@app.route('/ajax/post/up')
def ajax_uppost():
    if request.args.get('tid') :
        return jsonify(**try_set_flag(request.form.get('tid'),
                                      flag.UPVOTE))

@app.route('/ajax/post/star')
def ajax_starpost():
    return jsonify(**try_set_flag(request.form.get('tid'),
                                  flag.STAR))

@app.route('/ajax/post/update')
def ajax_postupdate():
    if request.form.get('tid'):
        tid = parse_int(request.form.get('tid'))
        if tid is None :
            return jsonify(error=1, msg="Wrong tid")
        if not request.form.get('title') :
            return jsonify(error=1, msg="Wrong title")
        db = getconn()
        ret = db.get(u"SELECT boardname, oldfilename FROM herzog_topic"
                     "  WHERE tid=%s", tid)
        if not ret :
            return jsonify(error=1, msg='No such topic')
        r = getclient().do_edit(board=ret.boardname,
                                title=request.form.get("title"),
                                file=ret.oldfilename,
                                text=request.form.get("text", ""))
        if 'success' in r :
            db.execute(u"UPDATE herzog_topic SET title=%s , content=%s"
                       "  WHERE tid=%s", request.form.get("title"),
                       request.form.get("text", ""), tid)
            return jsonify(success=1, msg="Update topic success")
        return jsonify(error=1, msg="Update topic failed")
    else :
        rid = parse_int(request.form.get('rid'))
        if rid is None:
            return jsonify(error=1, msg='Wrong rid')
        if not request.form.get('text') :
            return jsonify(error=1, msg='Wrong title')
        ret = db.get(u'SELECT tid, oldfilename FROM herzog_reply'
                     '  WHERE rid=%s', rid)
        if not ret :
            return jsonify(error=1, msg='No such reply')
        topic = db.get(u"SELECT title, boardname FROM herzog_topic"
                       "  WHERE tid=%s", ret.tid)
        r = getclient().do_edit(board=topic.boardname,
                                title=pf.quote_title(topic.title),
                                file=ret.oldfilename,
                                text=request.form.get("text"))
        if 'success' in r :
            db.execute(u"UPDATE herzog_topic SET content=%s"
                       "  WHERE rid=%s", request.form.get("text"))
            return jsonify(success=1, msg="Update reply success")
        return jsonify(error=1, msg="Update reply failed")

@app.route('/ajax/post/mark')
def ajax_markpost():
    userid = getuserid()
    params = dict(board=params['boardname'], mode=params['mode'])
    count = 0
    for k, v in request.form.items() :
        if k.startswith('r') :
            rid = parse_int(k[1:])
            if not rid : continue
            ret = db.get(u"SELECT oldfilename FROM herzog_reply"
                         "  WHERE rid=%s", rid)
            if not ret : continue
        elif k.startswith('t') :
            tid = parse_int(k[1:])
            if not tid : continue
            ret = db.get(u'SELECT oldfilename FROM herzog_topic'
                         '  WHERE tid=%s', tid)
            if not ret : continue
        params['box%s' % ret.oldfilename] = 1
        count = count + 1
        if count > 40 :
            break
    r = getconn().do_man(**params)
    return jsonify(**r)

@app.route('/ajax/post/_addv')
def ajax_addv():
    userid = getuserid()
    if is_sysop(userid) :
        tid = parse_int(request.form.get('tid'))
        v = parse_int(request.form.get('v'))
        db.execute(u"UPDATE herzog_topic SET v=%s WHERE tid=%s",
                   v, tid)
        return jsonify(success=1, msg="Success")
    else :
        abort(404)

# @app.route('/ajax/post/_recommend')
# def ajax_recommendpost():
#     # need to finish
#     userid = getuserid()
#     if is_sysop(userid) :
#         tid = parse_int(request.form.get('tid'))
#     return


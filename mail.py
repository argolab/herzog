from app import app, getclient, jsonify, render_template, request

@app.route('/l/')
def mail():
    mails = getclient().listmails(offset=1, limit=20)
    return render_template('mail.html', **mails)

@app.route('/ajax/mail/send', methods=["POST"])
def ajax_sendmail():
    userid = request.form.get('userid')
    title = request.form.get('title')
    text = request.form.get('text')
    if request.form.get('filenum') :
        return jsonify(error=1, emsg="No accept filenum param")
    if not (userid and title and text) :
        return jsonify(error=1,
                       emsg="Need all param userid, title, text")
    ret = getclient().do_sendmail(userid=userid.encode('utf8'),
                                  title=title.encode('utf8'),
                                  text=text.encode('utf8'))
    return jsonify(**ret)

@app.route('/ajax/mail/list')
def ajax_listmail():
    offset = request.args.get('offset', 1)
    try:
        limit = int(request.args.get('limit') or 20)
        if limit < 1 or limit > 40 :
            raise ValueError("Wrong limit param")
    except ValueError:
        return jsonify(error="1", emsg="Wrong limit param")
    mails = getclient().listmails(offset=offset, limit=limit)
    return jsonify(**mails)

@app.route('/ajax/mail/reply', methods=["POST"])
def ajax_replymail():
    userid = request.form.get('userid')
    title = request.form.get('title')
    text = request.form.get('text')
    try :
        filenum = request.form.get('num')
    except ValueError :
        filenum = None
    if not (userid and title and text and (filenum is not None)) :
        return jsonify(error=1,
                       emsg="Need all param userid, title, text, filenum")
    ret = getclient().do_sendmail(userid=userid.encode('utf8'),
                                  title=title.encode('utf8'),
                                  filenum=filenum,
                                  text=text.encode('utf8'))
    return jsonify(**ret)

@app.route('/ajax/mail/del', methods=["POST"])
def ajax_delmail():
    filenum = request.form.get('num')
    filename = request.form.get('filename')
    if not filename or not filename :
        return jsonify(error=1, emsg="Need all param num, filename")
    ret = getclient().do_delmail(filenum=filenum, filename=filename)
    return jsonify(**ret)

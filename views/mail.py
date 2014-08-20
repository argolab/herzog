from herzog.base import app, getclient, jsonify, render_template, request, ajax_fields_error

@app.route('/mail/')
def mail():
    offset = request.args.get('offset', 1)
    mails = getclient().listmails(offset=offset, limit=20)
    mails['offset'] = int(offset)
    return render_template('mail.html', limit=20, **mails)

@app.route('/ajax/mail/send', methods=["POST"])
@ajax_fields_error
def ajax_sendmail():
    form = getfields(_require=('userid', 'title', 'text'))
    ret = getclient().do_sendmail(userid=form['userid'].encode('utf8'),
                                  title=form['title'].encode('utf8'),
                                  text=form['text'].encode('utf8'))
    return jsonify(**ret)

# @app.route('/ajax/mail/list')
# @ajax_fields_error
# def ajax_listmail():
#     offset = request.args.get('offset', 1)
#     try:
#         limit = int(request.args.get('limit') or 20)
#         if limit < 1 or limit > 40 :
#             raise ValueError("Wrong limit param")
#     except ValueError:
#         return jsonify(error="1", emsg="Wrong limit param")
#     mails = getclient().listmails(offset=offset, limit=limit)
#     return jsonify(**mails)

@app.route('/ajax/mail/reply', methods=["POST"])
@ajax_fields_error
def ajax_replymail():
    form = getfields(_require=('userid', 'title', 'text', 'filenum'))
    ret = getclient().do_sendmail(userid=form['userid'].encode('utf8'),
                                  title=form['title'].encode('utf8'),
                                  filenum=form['filenum'],
                                  text=form['text'].encode('utf8'))
    return jsonify(**ret)

@app.route('/ajax/mail/del', methods=["POST"])
@ajax_fields_error
def ajax_delmail():
    form = getfields(_require=('filenum', 'filename'))
    ret = getclient().do_delmail(filenum=form['filenum'],
                                 filename=form['filename'])
    return jsonify(**ret)

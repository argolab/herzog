#-*- coding: utf-8 -*-

from herzog.base import app, getclient, jsonify, render_template, request, ajax_fields_error, authed, redirect, getconn, json_success, getbbsfile, getfields
from herzog.base.misc import getnow, filter_ansi, quote_title
from herzog.actions.new import topic, reply, comment
from herzog.actions.postship import upvote
from codecs import open
import re

@app.route('/mail/')
def mail():
    userid = authed()
    offset = request.args.get('offset', 1)
    mails = getclient().listmails(offset=offset, limit=20)
    if 'error' in mails :
        return render_template('mailstatus.html', **ret)
    mails['offset'] = int(offset)
    return render_template('mail.html', limit=20, userid=userid, **mails)

@app.route('/mail/<filename>')
def readmail(filename) :
    try:
        index = int(request.args.get('index'))
    except ValueError :
        return render_template('mailstatus.html', error=1, emsg=u'没有该邮件')
    mail = getclient().showmail(start=index)
    if mail.get('filename') == filename :
        mail['content'] = filter_ansi(open(getbbsfile(mail['@article']),
                                           encoding='gbk', errors='ignore').read())
        return render_template('readmail.html', index=index, mail=mail)
    else :
        return render_template('mailstatus.html', error=1, emsg=u'没有该邮件')

@app.route('/sendmail', methods=["POST", "GET"])
def sendmail():
    if request.method == 'POST' :
        form = getfields(_require=('userid', 'title', 'text'))
        ret = getclient().do_sendmail(userid=form['userid'].encode('utf8'),
                                      title=form['title'].encode('utf8'),
                                      text=form['text'].encode('utf8'))
        return render_template('mailstatus.html', **ret)
    else :
        return render_template('sendmail.html')

@app.route('/replymail/<filename>', methods=["POST", "GET"])
def replymail(filename):
    if request.method == 'POST' :
        form = getfields(_require=('userid', 'title', 'text', 'filenum'))
        ret = getclient().do_sendmail(userid=form['userid'].encode('utf8'),
                                      title=form['title'].encode('utf8'),
                                      filenum=form['filenum'],
                                      text=form['text'].encode('utf8'))
        return render_template('mailstatus.html', **ret)
    else :
        try:
            index = int(request.args.get('num'))
        except ValueError :
            return render_template('mailstatus.html', error=1, emsg=u'没有该邮件')
        mail = getclient().showmail(start=index)
        if mail.get('filename') == filename :
            title = quote_title(mail['title'])
            return render_template('replymail.html', title=title, index=index, mail=mail)
        else :
            return render_template('mailstatus.html', error=1, emsg=u'没有该邮件')            

@app.route('/ajax/mail/del', methods=["POST"])
@ajax_fields_error
def ajax_delmail():
    form = getfields(_require=('filenum', 'filename'))
    ret = getclient().do_delmail(filenum=form['filenum'],
                                 filename=form['filename'])
    return jsonify(**ret)

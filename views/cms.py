from herzog.base import app, getclient, render_template, abort, getfields, ajax_fields_error, authed, getconn
import json

@app.route('/page/manage')
def cms_manage():
    db = getconn()
    pages = db.query(u"SELECT pid, pagepath, pagename, lastupdate, lastuserid"
                     "  FROM herzog_cms_page")
    res = db.query(u"SELECT rid, resname, lastupdate, lastuserid"
                   "  FROM herzog_cms_resource")
    return render_template("cms_manage.html", pages=pages, res=res)
    
@app.route('/page/<path:pagename>')
def page(pagepath):
    db = getconn()
    pagedata = db.get(u'SELECT pagename, tpl, ds FROM herzog_cms_page'
                      '  INNER JOIN herzog_cms_resource'
                      '  ON herzog_cms_page.resname = '
                      '       herzog_cms_resource.rescname'
                      '  WHERE pagepath=%s', pagepath)
    if not pagedata :
        abort(404)
    if '.' in pagedata.tpl :
        abort(404)
    return render_template('cms/%s.html' % pagedata.tpl,
                           pagename=pagedata.pagename,
                           **json.loads(pagedata.ds))

@app.route('/page/preview')
def page_preview() :
    form = getfields(_require=('pagepath', 'pagename', 'ds'))
    db = getconn()
    pagedata = db.get(u"SELECT tpl FROM herzog_cms_page"
                      " WHERE pagepath=%s", form['pagepath'])
    if not pagedata :
        abort(404)
    return render_template('cms/%s.html' % pagedata.tpl,
                           pagename=form['pagename'],
                           **ds)

@app.route('/ajax/resource/update', methods=["POST"])
@ajax_fields_error
def update_resource():
    userid = authed()
    form = getfields(_require=('resname', 'ds'))
    try:
        json.loads(form['ds'])
    except ValueError :
        return json_error(3, "Wrong json value")
    db = getconn()
    rid = db.query(u"SELECT rid FROM herzog_cms_resource"
                   "  WHERE resname=%s", form['resname'])
    if rid :
        db.execute(u"UPDATE herzog_cms_resource SET"
                   "  resname=%s, ds=%s, lastuserid=%s"
                   " WHERE rid=%s",
                   form['resname'], form['ds'], userid, rid.rid)
    else :
        db.execute(u"INSERT INTO herzog_cms_resource"
                   "  resname, ds, lastuserid VALUES"
                   "  (%s, %s, %s)", form['resname'], form['ds'],
                   form['userid'])
    return json_success()

@app.route('/ajax/page/update', methods=["POST"])
@ajax_fields_error
def update_page():
    userid = authed()
    form = getfields(_require=('pagepath', 'pagename', 'tpl', 'rid'))
    db = getconn()
    pid = db.query(u"SELECT pid FROM herzog_cms_page"
                   "  WHERE pagepath=%s", form['pagepath'])
    if pid :
        if form['pagename'].strip() :
            db.execute(u"UPDATE herzog_cms_page SET"
                       "  pagename=%s, pagepath=%s, tpl=%s, rid=%s, lastuserid=%s",
                       "  WHERE pid=%s",
                       form['pagename'], form['pagepath'], form['tpl'],
                       form['rid'], userid, pid.pid)
        else :
            db.execute(u"DELETE FROM herzog_cms_page"
                       "  WHERE pid=%s", pid.pid)
    else :
        rid = db.execute(u"INSERT INTO herzog_cms_page"
                         "  pagename, pagepath, tpl, rid, lastuserid VALUES"
                         "  (%s, %s, %s, %s, %s)",
                         form['pagename'], form['pagepath'], form['tpl'],
                         form['rid'], userid)
    return json_success()

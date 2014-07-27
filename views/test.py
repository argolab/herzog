from herzog.base import (
    app, render_template, request, authed, getfields,
    ajax_fields_error, json_success, FormValidError,
    request
)

from herzog.actions.new import (
    topic as a_topic,
    reply as a_reply,
    comment as a_comment,
)

from herzog.actions.delete import (
    deltopic as a_deltopic,
    delreply as a_delreply,
    isowner_topic, isowner_reply
)

from herzog.actions.postship import (
    upvote as a_upvote, unvote as a_unvote,
    star as a_star, unstar as a_unstar,
    setv as a_setv
)

from herzog.actions.update import (
    update_topic as a_updatetopic,
    update_reply as a_updatereply
)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/ajax/post/update', methods=["POST"])
@ajax_fields_error
def ajax_updatepost():
    userid = authed()
    if request.form.get('tid') :
        form = getfields(_require=("tid", "title", "content"))
        form['userid'] = userid
        return json_success(**a_updatetopic(**form))
    else :
        form = getfields(_require=('rid', 'content'))
        form['userid'] = userid
        return json_success(**a_updatereply(**form))

@app.route('/ajax/post/newtopic', methods=['POST'])
@ajax_fields_error
def ajax_newtopic():
    userid = authed()
    form = getfields(_require=('boardname', 'title', 'content'),
                      _optional=('summary',))
    form['userid'] = userid
    form['fromaddr'] = request.remote_addr
    ret = a_topic(**form)
    return json_success(**ret)

@app.route('/ajax/post/reply', methods=['POST'])
@ajax_fields_error
def ajax_reply():
    userid = authed()
    form = getfields(_require=("content",),
                     _optional=("tid", "replyid", "summary"))
    if not form.has_key('tid') and not form.has_key('replyid') :
        raise FormValidError('Must supply tid or replyid')
    form['userid'] = userid
    form['fromaddr'] = request.remote_addr
    if form.has_key('tid') :
        ret = a_reply(**form)
    else :
        ret = a_comment(**form)
    return json_success(**ret)
                
@app.route('/ajax/post/del', methods=["POST"])
@ajax_fields_error
def ajax_delpost():
    userid = authed()
    form = getfields(_require=(), _optional=("tid", "rid"))
    if not form.has_key('tid') and not form.has_key('rid') :
        raise FormValidError('Must supply tid or replyid')
    if form.has_key('tid') :
        ret = a_deltopic(userid, form['tid'])
    else :
        ret = a_delreply(userid, form['rid'])
    return json_success(**ret)

@app.route('/ajax/post/star', methods=["POST"])
@ajax_fields_error
def ajax_starpost():
    userid = authed()
    form = getfields(_require=(), _optional=("tid", "rid"))
    if not form.has_key('tid') and not form.has_key('rid') :
        raise FormValidError('Must supply tid or replyid')
    return json_success(**a_star(userid, form.get('tid'), form.get('rid')))

@app.route('/ajax/post/unstar', methods=["POST"])
@ajax_fields_error
def ajax_unstarpost():
    userid = authed()
    form = getfields(_require=(), _optional=("tid", "rid"))
    if not form.has_key('tid') and not form.has_key('rid') :
        raise FormValidError('Must supply tid or replyid')
    return json_success(**a_unstar(userid, form.get('tid'), form.get('rid')))

@app.route('/ajax/post/upvote', methods=["POST"])
@ajax_fields_error
def ajax_upvotepost():
    userid = authed()
    form = getfields(_require=(), _optional=("tid", "rid"))
    if not form.has_key('tid') and not form.has_key('rid') :
        raise FormValidError('Must supply tid or replyid')
    return json_success(**a_upvote(userid, form.get('tid'), form.get('rid')))

@app.route('/ajax/post/unvote', methods=["POST"])
@ajax_fields_error
def ajax_unvotepost():
    userid = authed()
    form = getfields(_require=(), _optional=("tid", "rid"))
    if not form.has_key('tid') and not form.has_key('rid') :
        raise FormValidError('Must supply tid or replyid')
    return json_success(**a_unvote(userid, form.get('tid'), form.get('rid')))

@app.route('/ajax/post/setv', methods=["POST"])
@ajax_fields_error
def ajax_setvpost():
    userid = authed()
    form = getfields(_require=("tid", "v"))
    return json_success(**a_setv(userid, form.get('tid'), form.get('v')))



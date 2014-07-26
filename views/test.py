from herzog.base import (
    app, render_template, request, authed, getfields,
    ajax_fields_error, json_success, FormValidError
)

from herzog.actions.new import (
    topic as a_topic,
    reply as a_reply,
    comment as a_comment
)
    
@app.route('/')
def index():
    return render_template('test.html')

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
                

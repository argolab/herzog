from app import app, render_template, _j

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

@app.route('/ajax/post/list')
def ajax_listpost():
    return

@app.route('/ajax/post/new')
def ajax_newpost():
    return

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

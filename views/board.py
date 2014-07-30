from herzog.base import app, render_template, getconn, getclient, abort

@app.route('/b/<boardname>')
def board(boardname):
    db = getconn()
    board = getclient().showboard(board=boardname)
    if 'error' in board :
        abort(404)
    topics = db.query(u"SELECT tid, owner, title, score, v, lastupdate,"
                      "   lastreply, replynum, partnum, upvote, fromapp,"
                      "   flag, content FROM herzog_topic WHERE boardname=%s"
                      "  ORDER BY score DESC LIMIT 15", boardname)
    bsetting = {
        "image" : "/static/img/85.jpg"
    }
    return render_template('board.html', board=board, bsetting=bsetting,
                           topics=topics)

#-*- coding: utf-8 -*-

from herzog.base import app, render_template, getconn, getclient, abort, authed, getuserid, getboards
import json

def getbsetting(boardname) :
    bsetting = getconn().get(u"SELECT ds FROM herzog_cms_resource"
                             "  WHERE resname='site::bsetting'")
    if not bsetting :
        return None
    bsetting = json.loads(bsetting['ds'])
    for it in bsetting['boards']['list'] :
        if it['info']['title'] == boardname :
            return it
    return None

def get_all_bsetting() :
    bsetting = getconn().get(u"SELECT ds FROM herzog_cms_resource"
                             "  WHERE resname='site::bsetting'")
    if not bsetting :
        return None
    bsetting = json.loads(bsetting['ds'])
    bs = {}
    for it in bsetting['boards']['list'] :
        bs[it['info']['title']] = it
    return bs

@app.route('/b/<boardname>')
def board(boardname):
    db = getconn()
    board = getclient().showboard(board=boardname)
    if 'error' in board :
        abort(404)
    userid = getuserid()
    if userid :
        topics = db.query(u"SELECT herzog_topic.tid, owner, title, score, v, lastupdate,"
                          "   lastreply, replynum, partnum, upvote, fromapp, readtime,"
                          "   herzog_topicship.flag, content, upvote, boardname, herzog_topicship.flag as tsflag, readtime FROM herzog_topic"
                          "  LEFT JOIN herzog_topicship"
                          "    ON herzog_topicship.tid=herzog_topic.tid AND userid=%s"
                          "  WHERE boardname=%s"
                          "  ORDER BY score DESC LIMIT 16", userid, boardname)
    else :
        topics = db.query(u"SELECT tid, owner, title, score, v, lastupdate,"
                          "   lastreply, replynum, partnum, upvote, fromapp,"
                          "   flag, content, upvote, boardname FROM herzog_topic"
                          " WHERE boardname=%s ORDER BY score DESC LIMIT 16", boardname)
    if len(topics) == 16 :
        score = topics[-1].score
        del topics[15]
    else :
        score = -1
    bsetting = getbsetting(boardname) or dict()
    print bsetting
    return render_template('board.html', board=board, bsetting=bsetting,
                           topics=topics)

def groupup(boards) :
    sections = {}
    for name, x in boards.items() :
        secnum = int(x['secnum'])
        if not secnum in sections :
            sections[secnum] = []
        sections[secnum].append(x)
    return sections

secdatas = [
    u"BBS 系统",
    u"校园社团",
    u"院系交流",
    u"电脑科技",
    u"休闲娱乐",
    u"文化艺术",
    u"学术科学",
    u"谈天说地",
    u"社会信息",
    u"体育健身",
]

@app.route('/b/all')
def allboard():
    boards = getboards()
    sections = groupup(boards)
    bs = get_all_bsetting()
    if authed() :
        msg = getclient().getmessage()
    else :
        msg = None
    return render_template('allboards.html', secdatas=secdatas,
                           boards=boards, sections=sections, bs=bs, msg=msg)

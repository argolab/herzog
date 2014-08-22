from herzog.base import app, getconn, render_template, getclient, getboards
from herzog.base.jstore import hzd

def groupup(topics) :
    ind = {}
    d = []
    boards = getboards()
    for t in topics :
        if t.boardname not in ind :
            ind[t.boardname] = len(d)
            d.append({
                'boardname' : t.boardname,
                'boarddesc' : boards[t.boardname]['boarddesc'],
                'posts' : []
            })
        d[ind[t.boardname]]['posts'].append(t)
    return d

@app.route('/!')
def testpage():
    return render_template('test.html')

@app.route('/')
def index():
    db = getconn()
    topics = db.query(u"SELECT tid, owner, title, score, v, lastupdate,"
                      "   lastreply, replynum, partnum, upvote, fromapp,"
                      "   flag, content, boardname FROM herzog_topic"
                      "  ORDER BY score DESC LIMIT 21")
    if len(topics) == 21 :
        score = topics[-1].score
        del topics[20]
    else :
        score = -1
    boards = getclient().allboards()
    # Filter the topics use a whitelist
    fresh = groupup(topics)
    # TODO : topics may be NONE
    # TODO : perm filter
    # TODO : fresh and topten
    topten = [ dict(title=t.title, tid=t.tid, owner=t.owner)
               for t in topics[:10] ]
    img = hzd.get('page:fresh:image')
    goods = hzd.geta('page:fresh:goods')
    ad = hzd.geto('pgae:fresh:ad')
    return render_template('fresh.html', fresh=fresh, img=img,
                           boards=boards, score=score,
                           topten=topten, goods=goods, ad=ad)

@app.route('/ajax/fresh/list')
def fresh():
    try :
        score = float(request.args.get('cursor'))
    except ValueError :
        return json_error('wrong cursor')
    topics = db.query(u"SELECT tid, owner, title, score, v, lastupdate,"
                      "   lastreply, replynum, partnum, upvote, fromapp,"
                      "   flag, content, boardname FROM herzog_topic"
                      "  WHERE score <= %s"
                      "  ORDER BY score DESC LIMIT 21", score)
    if len(topics) == 21 :
        score = topics[-1].score
        del topics[20]
    else :
        score = -1
    fresh = groupup(topics)
    return render_template('fresh-append.html', fresh=fresh, score=score)
    
    

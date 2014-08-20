from herzog.base import app, getconn, render_template
from herzog.base.jstore import hzd

def groupup(topics) :
    ind = {}
    d = []
    for t in topics :
        if t.boardname not in ind :
            ind[t.boardname] = len(d)
            d.append({
                'boardname' : t.boardname,
                'posts' : []
            })
        d[ind[t.boardname]]['posts'].append(t)
    return d

@app.route('/')
def index():
    db = getconn()
    topics = db.query(u"SELECT tid, owner, title, score, v, lastupdate,"
                      "   lastreply, replynum, partnum, upvote, fromapp,"
                      "   flag, content, boardname FROM herzog_topic"
                      "  ORDER BY score DESC LIMIT 20")
    # Filter the topics use a whitelist
    fresh = groupup(topics)
    print fresh
    # TODO : topics may be NONE
    # TODO : perm filter
    # TODO : fresh and topten
    topten = [ dict(title=t.title, tid=t.tid, owner=t.owner)
               for t in topics[:10] ]
    img = hzd.get('page:fresh:image')
    goods = hzd.geta('page:fresh:goods')
    ad = hzd.geto('pgae:fresh:ad')
    return render_template('fresh.html', fresh=fresh, img=img,
                           topten=topten, goods=goods, ad=ad)

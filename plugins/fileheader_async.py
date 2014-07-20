from app import app, bind, Precondition, getclient, g, getconn

# def save2fh(boardname, title, userid, fromaddr, content,

@bind('require_newtopic')            
def save2fh(boardname, title, userid, fromaddr, content, summary):
    ret = getclient().do_snd(board=boardname, title=title,
                             text=content)
    if 'error' in ret :
        raise Precondition('NewTopicError', message=ret['emsg'])
    g._fa_filename = ret['filename']
    
@bind('success_newtopic')
def g_update_filename(tid, **data):
    db = getconn()
    db.execute(u" UPDATE herzog_topic SET oldfilename=%s WHERE tid=%s",
               g._fa_filename, tid)

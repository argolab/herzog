from app import app, bind, Precondition, getclient, g, getconn, pf

# def save2fh(boardname, title, userid, fromaddr, content,

@bind('require_newtopic')            
def g_save2fh(boardname, title, userid, fromaddr, content, summary):
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

@bind('require_reply')
def g_save2fh_reply(tid, brid, replyid, userid, content, fromaddr):
    db = getconn()
    if replyid == 0 :
        origin = db.get(u"SELECT boardname, oldfilename, title, content,"
                        "     owner FROM herzog_topic WHERE tid=%s", tid)
        if not origin :
            raise Precondition("ReplyError", message="No such post")
    else :
        origin = db.get(u"SELECT tid, title, oldfilename, content, owner"
                        " FROM herzog_reply WHERE rid=%s", replyid)
        if not origin :
            raise Precondition("ReplyError", message="No such post")
        torigin = db.get(u"SELECT boardname FROM herzog_topic"
                         " WHERE tid=%s", origin.tid)
        if not torigin :
            raise Precondition("ReplyError", message="No such topic")
        origin.boardname = torigin.boardname
    print repr(pf.quote(origin.content, origin.owner))
    content = content + pf.quote(origin.content, origin.owner)
    ret = getclient().do_snd(board=origin.boardname,
                             title=pf.quote_title(origin.title),
                             text=content.encode('utf8'),
                             refile=origin.oldfilename)
    if 'success' in ret :
        g._fa_filename = ret['filename']
    else :
        raise Precondition('ReplyError', message=ret['emsg'])
        
@bind('success_reply')
def g_update_filename_reply(rid, replyid, utid):
    db = getconn()
    db.execute(u"UPDATE herzog_reply SET oldfilename=%s WHERE rid=%s",
               g._fa_filename, rid)

    

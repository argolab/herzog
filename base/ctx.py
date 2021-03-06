#-*- coding: utf-8 -*-

from herzog.base.exception import FormValidError
from herzog.base.app import g, session, request
from herzog.base.torndb import Connection
from herzog.base.argorpc import ArgoRPCClicent
import herzog.config as config

def getclient():
    if not hasattr(g, 'cc'):
        g.cc = ArgoRPCClicent(session,
                              request.remote_addr)
    return g.cc

def getconn():
    if not hasattr(g, 'db'):
        g.db = Connection(config.DB_HOST, config.DB_DATABASE,
                          user=config.DB_USER,
                          password=config.DB_PASSWORD)
    return g.db
    
def authed():
    try : 
        return session.get('utmpuserid')
    except KeyError :
        raise FormValidError("Please login first")

def getuserid():
    return session.get('utmpuserid') or None

def getboards():
    if not session.has_key('boards_can_read') :
        data = getclient().allboards()['boards']
        bs = {}
        for board in data :
            bs[board['boardname']] = board
        session['boards_can_read'] = bs
    return session['boards_can_read']

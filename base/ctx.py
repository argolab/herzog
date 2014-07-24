#-*- coding: utf-8 -*-

from herzog.base.app import g, session
from herzog.base.torndb import Connection
from herzog.base.argorpc import ArgoRPCClicent
import herzog.config as config

def getclient():
    if not hasattr(g, 'cc'):
        g.cc = argorpc.ArgoRPCClicent(session,
                                      request.remote_addr)
    return g.cc

def getconn():
    if not hasattr(g, 'db'):
        g.db = Connection(config.DB_HOST, config.DB_DATABASE,
                          user=config.DB_USER,
                          password=config.DB_PASSWORD)
    return g.db
    
def getuserid():
    return session.get('utmpuserid') or None



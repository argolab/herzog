from flask import (
    Flask,
    g,
    request,
    session,
    url_for,
    abort,
    render_template,
    flash,
    session,
    jsonify
)
import json
from utils import event
from utils.event import Precondition
from utils.torndb import Connection
import argorpc
from argorpc import getbbsfile, getuserfile
from datetime import datetime as dt
from utils import flag

import config

app = Flask(__name__)

app.secret_key = config.SECRET_KEY
    
def _j(name):
    return json.load(open('devdata/%s.json' % name))

@app.context_processor
def inject_site_config():
    return dict(site=config.site, user=_j('user'))

def getclient():
    if not hasattr(g, 'cc'):
        g.cc = argorpc.ArgoRPCClicent(session,
                                      request.remote_addr)
    return g.cc

_DBHOST = config.DB_HOST
_DBUSER = config.DB_USER
_DBPASSWORD = config.DB_PASSWORD
_DBDBNAME = config.DB_DATABASE

def getconn():
    if not hasattr(g, 'db'):
        g.db = Connection(_DBHOST, _DBDBNAME, user=_DBUSER,
                          password=_DBPASSWORD)
    return g.db

def getuserid():
    return session.get('utmpuserid') or None

def getnow():
    return dt.now()

def parse_int(k, min, max, default):
    try:
        k = int(k)
    except (TypeError, ValueError):
        return default
    if k < min or k >= max :
        return default

@app.template_filter('postHtml')
def post_html(text):
    return text.replace('\n', '<br>')

@app.template_global('url_for_avatar')
def url_for_avatar(author):
    return 'http://bbs.sysu.edu.cn/avatar/%s' % author

_es = event.EventServer()
bind = _es.bind
trigger = _es.trigger
register_event = _es.register

register_event(
    "require_newtopic",
    '''
    Precondition of post a new post.
      [tid, boardname, title, userid, fromaddr, content, summary]
      --> message  , message to return to user'''
)    

register_event(
    "success_newtopic",
    '''Trigger after add a new topic success. 
         [tid, boardname, title, userid, fromaddr, content, summary]'''
)



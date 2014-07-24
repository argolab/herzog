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
from utils import pf
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

def parse_range(k, min, max, default):
    try:
        k = int(k)
    except (TypeError, ValueError):
        return default
    if k < min or k >= max :
        return default

def parse_int(k, default=None):
    try:
        return int(k)
    except (TypeError, ValueError):
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

try :
    sysops = set(getbbsfile('etc/SYSOPS.herzog').read().split())
except IOError :
    print 'Cannot load sysops name. Check your BBS_HOME/etc/SYSOP.herzog file'
    sysops = set()
    
def is_sysop(x):
    return x in sysops

register_event(
    "require_newtopic",
    '''
    Precondition of post a new post.
      [tid, boardname, title, userid, fromaddr, content, summary]
      --> message  , fatal message to return to user'''
)    

register_event(
    "success_newtopic",
    '''Trigger after add a new topic success. 
         [tid, boardname, title, userid, fromaddr, content, summary]'''
)

register_event(
    'require_reply',
    '''
    Precondition of reply a topic or reply.
      [tid, brid, replyid, userid, content, fromaddr]
      -> message  , fatal message to return to user'''
)

register_event(
    'success_reply',
    '''Trigger after reply.
      [rid, replyid, utid]'''
)

class FormValue(dict):

    def __getattr__(self, name) :
        try:
            return self[name]
        except KeyError:
            return None

    def __setattr__(self, name, value) :
        self[name] = value

class ValidError(Exception) :

    def __init__(self, msg, **params):
        self.message = msg
        self.params = params

def add_success_field(key, value):
    if not hasattr(g, 'success') :
        g.success = {}
    g.success[key] = value

def json_success(**params):
    if hasattr(g, 'success') :
        params.update(g.success)
    return jsonify(success=1, **params)

def json_error(e) :
    return jsonify(error=e.message, **e.params)

def valid(form, _require=(), _optional=(), _extra=None, **typer):
    ret = {}
    missing = []
    if _require :
        for name in _require :
            field = form.get(name, None)
            if field is None :
                missing.append(name)
                continue
            if name in typer :
                try :
                    ret[name] = typer[name](field)
                except (TypeError, ValueError) :
                    raise ValidError('Wrong %s value' % name,
                                     name=name, value=form.get(value))
                continue
            ret[name] = field
    if _optional :
        for name in _optional :
            field = form.get(name, None)
            if field is None :
                continue
            if name in typechecker :
                try :
                    ret[name] = typer[name](field)
                except (TypeError, ValueError) :
                    raise ValidError('Wrong %s value' % name,
                                     name=name, value=form.get(value))
                continue
            ret[name] = field
    if missing :
        raise ValidError('Missing params %s' % (','.join(missing)),
                         missing=missing)
    if _extra :
        ret.update(_extra)        
    return ret


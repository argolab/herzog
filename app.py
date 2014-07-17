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

import argorpc
from argorpc import getbbsfile, getuserfile

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

@app.template_filter('postHtml')
def post_html(text):
    return text.replace('\n', '<br>')

@app.template_global('url_for_avatar')
def url_for_avatar(author):
    return 'http://bbs.sysu.edu.cn/avatar/%s' % author

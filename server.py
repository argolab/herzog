from flask import Flask, request, session, url_for, abort,\
         render_template, flash, session, g, jsonify
import json
import argorpc
from argorpc import read_bbsfile
import config

app = Flask(__name__)

def _j(name):
    return json.load(open('devdata/%s.json' % name))

@app.context_processor
def inject_site_config():
    return dict(site=config.site, user=_j('user'))

def get_client():
    if not hasattr(g, 'cc'):
        g.cc = argorpc.ArgoRPCClicent(session,
                                      request.remote_addr)
    return g.cc

@app.template_filter('postHtml')
def post_html(text):
    return text.replace('\n', '<br>')

@app.route('/')
def fresh():
    return render_template('fresh.html', **_j('fresh'))

@app.route('/v/topten')
def topten():
    return render_template('topten.html',
                           **_j('topten'))

@app.route('/b/<boardname>')
def board(boardname):
    return '1'

@app.route('/r/<int:topicid>')
def topic(topicid):
    return render_template('topic.html',
                           **_j('topic'))

@app.route('/u/<userid>')
def user(userid):
    user = get_client().queryuser(userid=userid)
    if '@plans' in user :
        user['plans'] = read_bbsfile(user['@plans'])
    return render_template('query_user.html', user=user)

@app.route('/t/notifications')
def notifications():
    return 1

@app.route('/t/mail')
def mail():
    return 1

@app.route('/t/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/t/logout', methods=['POST'])
def logout():
    return 1

@app.route('/t/setting')
def setting():
    return 1

@app.route('/ajax/do/good', methods=['POST'])
def good():
    return 1

@app.route('/ajax/reply')
def reply():
    return 1

@app.route('/ajax/do/thinks')
def thinks():
    return 1

app.secret_key = config.SECRET_KEY

if __name__ == '__main__' :
    app.run(host="0.0.0.0", debug=True)


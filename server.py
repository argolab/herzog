from flask import Flask, request, session, url_for, abort,\
         render_template, flash, session, g, jsonify

import argorpc

import config

app = Flask(__name__)

def get_client():
    if not hasattr(g, 'cc'):
        g.cc = argorpc.ArgoRPCClicent(session,
                                      request.remote_addr)
    return g.cc

@app.route('/u/<userid>')
def query_user(userid):
    return render_template('query_user.html',
                           user=get_client().queryuser(userid=userid))

@app.route('/t/login')
def login():
    return render_template('login.html')

@app.route('/ajax/2/login', methods=['POST'])
def ajax_login():
    userid = request.form['userid']
    password = request.form['password']
    ret = get_client().do_login(id=userid, pw=password)
    return jsonify(**ret)

app.secret_key = config.SECRET_KEY

if __name__ == '__main__' :
    app.run(debug=True)


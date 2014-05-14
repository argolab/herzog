from flask import Flask, request, session, url_for, abort,\
         render_template, flash, session, g

import argorpc

import config

app = Flask(__name__)

def get_client():
    if not hasattr(g, 'cc'):
        g.cc = argorpc.ArgoRPCClicent(session)
    return g.cc

@app.route('/u/<userid>')
def query_user(userid):
    return render_template('query_user.html',
                           **get_client().queryuser(userid=userid))

if __name__ == '__main__' :
    app.run(debug=True)


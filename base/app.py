from flask import (
    Flask, g, request, session, url_for,
    abort, render_template, session, jsonify
)
import herzog.config as config

app = Flask('herzog')
app.secret_key = config.SECRET_KEY

route = app.route

def start_server(**kwargs):
    import herzog.base
    app.run(**kwargs)

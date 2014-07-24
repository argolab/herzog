from flask import (
    Flask, g, request, session, url_for,
    abort, render_template, session, jsonify
)

import os.path

app = Flask('herzog')

route = app.route

def start_server(**kwargs):
    import herzog.base
    app.run(**kwargs)

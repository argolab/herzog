#-*- coding: utf-8 -*-

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

import herzog.config as config

app = Flask(__name__)

app.secret_key = config.SECRET_KEY
    

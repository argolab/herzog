from flask import (
    Flask, g, request, session, url_for,
    abort, render_template, session, jsonify,
    redirect
)
import herzog.config as config

app = Flask('herzog')
app.secret_key = config.SECRET_KEY

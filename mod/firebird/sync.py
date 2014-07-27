from herzog.base import app
from herzog.base.log import getlogger

logger = getlogger(__name__)

@app.route("/_hfb/post/reply")
def sync_reply(b, f, f0):
    pass

@app.route("/_hfb/post/newtopic")
def sync_newtopic(b, f, f0):
    pass

@app.route("/_hfb/post/cross")
def async_cross(b, f, f0):
    pass

@app.route("/_hfb/post/changetitle")    
def sync_update_title(b, f, f0):
    pass

@app.route("/_hfb/post/updatepost")
def sync_update_content(b, f, f0):
    pass

@app.route("/_hfb/post/del")
def sync_delete(b, f, f0):
    pass


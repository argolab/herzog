from herzog.base.app import app, session
from herzog.base.ctx import authed, getclient, getboards, getuserid
from herzog import config
from herzog.base import flag

@app.context_processor
def inject_site_config():
    return dict(site=config.SITE, FLAG=flag)

@app.template_filter(name='read_board_perm')
def read_board_perm(boardname):
    return boardname in getboards()

@app.template_filter(name='nicetime')
def nicetime(dt):
    return str(dt)

@app.template_filter()
def postHtml(text):
    return text.replace('\n', '<br>')

@app.template_global('url_for_avatar')
def url_for_avatar(author):
    return 'http://bbs.sysu.edu.cn/avatar/%s' % author

@app.template_global('url_for_ann')
def url_for_ann(boardname):
    return ''

app.template_global()(authed)
app.template_global()(getuserid)

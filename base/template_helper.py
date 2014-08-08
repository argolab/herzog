from herzog.base.app import app
from herzog.base.ctx import authed
from herzog import config

@app.context_processor
def inject_site_config():
    return dict(site=config.SITE)

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

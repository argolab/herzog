from herzog.app import app

@app.context_processor
def inject_site_config():
    return dict(site=config.site, user=_j('user'))

@app.template_filter('postHtml')
def post_html(text):
    return text.replace('\n', '<br>')

@app.template_global('url_for_avatar')
def url_for_avatar(author):
    return 'http://bbs.sysu.edu.cn/avatar/%s' % author

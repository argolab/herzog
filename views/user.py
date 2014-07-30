from herzog.base import app, getclient, render_template

@app.route('/u/<userid>')
def user(userid):
    user = getclient().queryuser(userid=userid)
    if '@plans' in user :
        user['plans'] = read_bbsfile(user['@plans'])
    return render_template('query_user.html', user=user)


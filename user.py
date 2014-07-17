from app import app, getclient

@app.route('/u/<userid>')
def user(userid):
    user = get_client().queryuser(userid=userid)
    if '@plans' in user :
        user['plans'] = read_bbsfile(user['@plans'])
    return render_template('query_user.html', user=user)


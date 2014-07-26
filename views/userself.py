from herzog.base import (
    app, render_template, getclient, json_success,
    session, json_error, authed, ajax_fields_error,
    getfields, request
)

@app.route('/ajax/login', methods=["POST"])
@ajax_fields_error
def login():
    form = getfields(('userid', 'password'))
    print form
    cli = getclient()
    ret = cli.do_login(id=form['userid'], pw=form['password'])
    if ret.get('success') :
        return json_success()
    else :
        return json_error(3, ret['emsg'])

@app.route('/ajax/logout', methods=['POST'])
def logout():
    authed()
    ret = getclient().do_logout()
    if ret.get('success') :
        session.clear()
        return json_success()
    return json_error(4, ret['emsg'])

# @app.route('/ajax/setting', methods=["POST"])
# def setting():
#     if not session.get('utmpuserid') :
#         return jsonify(error=1, msg="No login")
#     userid = session.get('utmpuserid')

#     if request.form.get('!clear!') :
#         getuserfile(userid, 'setting.json', mode='w').write('{}')
#         return jsonify(success=1, error='clear setting success!')
    
#     try :
#         data = json.load(getuserfile(userid, 'setting.json', 'r'))
#     except :
#         data = {}

#     data.update(request.form)

#     ds = json.dumps(data)
#     if len(data) > 4096 :
#         return jsonify(error=1, msg="Save too many value to dict!")
#     getuserfile(userid, 'setting.json', 'w').write(ds)
#     return jsonify(success=1, msg='Update setting success!')

from app import (
    app, request, render_template,
    jsonify, getclient, getuserfile,
    json, session
)

@app.route('/ajax/login', methods=["POST"])
def login():
    userid = request.form.get('userid', None)
    password = request.form.get('password', None)
    if not userid or not password :
        return jsonify(error=1, msg="Need userid, password param")
    cli = getclient()
    ret = cli.do_login(id=userid, pw=password)
    if ret.get('success') :
        return jsonify(success=1, msg='Login success.')
    else :
        return jsonify(ret)

@app.route('/ajax/logout', methods=['POST'])
def logout():
    ret = getclient().do_logout()
    if ret.get('success') :
        session.clear()
        return jsonify(ret)
    return jsonify(ret)

@app.route('/ajax/setting', methods=["POST"])
def setting():
    if not session.get('utmpuserid') :
        return jsonify(error=1, msg="No login")
    userid = session.get('utmpuserid')

    if request.form.get('!clear!') :
        getuserfile(userid, 'setting.json', mode='w').write('{}')
        return jsonify(success=1, error='clear setting success!')
    
    try :
        data = json.load(getuserfile(userid, 'setting.json', 'r'))
    except :
        data = {}

    data.update(request.form)

    ds = json.dumps(data)
    if len(data) > 4096 :
        return jsonify(error=1, msg="Save too many value to dict!")
    getuserfile(userid, 'setting.json', 'w').write(ds)
    return jsonify(success=1, msg='Update setting success!')

def getusersetting():
    # may by form is array ? (name:[key])
    if not session.get('utmpuserid') :
        return None
    try :
        return json.load(getuserfile(session.get('utmpuserid'),
                                     'setting.json'))
    except IOError :
        return {}
        

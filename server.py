from herzog.base import app

import herzog.views.test
__import__("herzog.mod.firebird")

# from app import app

# app.config['DEBUG'] = True

# if app.config['DEBUG'] :
#     import debug

# import topic
# import mail
# import user
# import notice
# import picture
# import userself
# import plugins.fileheader_async

if __name__ == '__main__' :
    app.run(host="0.0.0.0", port=8080, debug=True)

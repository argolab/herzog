# import watchless
# watchless.main()

from app import app, request
from flask import render_template
from userself import getusersetting

@app.route('/t')
def test():
    return render_template('test.html', setting=getusersetting())

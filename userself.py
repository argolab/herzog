from app import app

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/t/logout', methods=['POST'])
def logout():
    return 1
    
@app.route('/t/setting')
def setting():
    return 1

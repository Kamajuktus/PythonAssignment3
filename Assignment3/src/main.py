from datetime import datetime, timedelta
from flask import Flask, request, redirect
from flask.helpers import make_response, url_for
from flask_sqlalchemy import SQLAlchemy
import jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:333btybfRA@127.0.0.1:5432/PythonAs3'
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
db = SQLAlchemy(app)

token = ''

class UserTable(db.Model):
    __tablename__ = 'userr'
    id = db.Column('id', db.Integer, primary_key = True)
    login = db.Column('login', db.Unicode)
    password = db.Column('password', db.Integer)
    token = db.Column('login', db.Unicode)

    def __init__(self, id, login, password, token):
        self.id = id
        self.login = login
        self.password = password
        self.token = token

@app.route('/login')
def login():

    auth = request.authorization

    select_this = UserTable.query.filter_by(login=auth).first()

    if auth and auth.password == select_this.password:
        
        return redirect(url_for('getToken', auth=auth))
    
    return make_response('Could not find a user with login: ' + auth, 401, {'WWW-Authenticate': 'Basic realm="Login required'})

def token_required(var):
    def wrapper(func):
        if var != None:
            return func
        else:
            return '<h1>Hello, could not verify the token</h1>'
    return wrapper
    
@app.route('/getToken')
def getToken():
    auth = request.args.get('auth')
    token = jwt.encode({'user':auth.username, 'exp':datetime.utcnow() + timedelta(minutes=5)}, app.config['SECRET_KEY'])
    return redirect(url_for('somethingElse', var=token))

@app.route('/protected')
@token_required
def somethingElse():
    return '<h1>Hello, token which is provided is correct</h1>'

if __name__ == '__main__':
    app.run(debug=True)
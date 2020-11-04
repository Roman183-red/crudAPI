import json
from flask import Flask, render_template, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/status')
def status():
    return 'app is running'


@app.route('/users')
def users():
    users = User.query.all()
    return jsonify(str(users))


@app.route('/user/<username>')
def user(username):
    user = User.query.filter(User.username==username).first()
    if not user:
        abort(404)
    return jsonify(str(user))


@app.route('/user/create', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json:
        abort(400)
    user = User(username=request.json['username'], email=request.json['email'])
    
    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()

    return jsonify({'user': str(user)}), 200
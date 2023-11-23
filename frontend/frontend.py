#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Frontend service
#
import os
import json
import random
import string

from functools import wraps

from flask import Flask, render_template, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, exc, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from redis import Redis

# Global Config
basedir = os.path.abspath(os.path.dirname(__file__))
db_user = os.environ['POSTGRES_USER']
db_pass = os.environ['POSTGRES_PASSWORD']
db_host = "info-db"
db_port = "5432"
db_name = os.environ['POSTGRES_DB']
db_uri = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

# Application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config.from_object(os.environ['APP_SETTINGS'])

# DB Session
db = SQLAlchemy(app)

# Redis
redis = Redis(host='info-redis', port=6379)

# Models
class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    biography = db.Column(db.Text)

    def __repr__(self):
        return f'<Account {self.firstname} {self.lastname} {self.email}>'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Functions
def generate_string(length):
    import random
    import string
    result = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result

def generate_number(minimum=1, maximum=100):
    return random.randint(minimum, maximum)

# Routes
@app.route("/")
@app.route("/hello")
def index():
    return render_template('index.html')

@app.route("/hi")
@app.route("/hi/<name>")
def hi(name=None):
    if name:
        return jsonify({"data": "hi, %s" % name}), 200
    else:
        return jsonify({"data": "hi"}), 200

@app.route("/ping")
def ping():
    return jsonify({"response": "pong"}), 200

@app.route('/redis')
def hello():
    redis.incr('hits')
    views = int.from_bytes(redis.get('hits'))
    print('Redis views: %d' % views, flush=True)
    return jsonify({"data": str(views)}), 200

@app.route('/add')
def add_user():
    firstname = generate_string(generate_number(4, 8))
    lastname = generate_string(generate_number(4, 9))
    new_account = Account(firstname=firstname,
                          lastname=lastname,
                          email=f'{firstname}.{lastname}@example.com',
                          age=generate_number(18, 112),
                          biography='Random user')
    db.session.add(new_account)
    db.session.commit()
    return jsonify({"data": str(new_account.account_id)}), 200


@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = db.session.query(Account).all()
    return jsonify({"data": [a.as_dict() for a in accounts]}), 200

@app.route('/accounts/<int:id>')
def get_account():
    id = request.args.getlist('id', type=int)
    return jsonify({"data": f'Details for account {id}'}), 200

@app.route('/init')
def init():
    output = ""
    # Initialise database
    from sqlalchemy_utils import database_exists, create_database
    engine = create_engine(db_uri)
    if not database_exists(engine.url):
        create_database(engine.url)
        output += "Database does not exist, creating. "
    try:
       db.drop_all()
       output += "All tables dropped. "
    except Exception:
       pass
    db.create_all()
    output += "All tables created."
    return jsonify({"data": output.strip()}), 200

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404


# # Authentication
# def authenticated(func):
#     """Checks whether user is logged in or raises error 401."""
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if session.get('admin_user', False):
#             return func(*args, **kwargs)
#         else:
#             return jsonify({"data": {}, "error": "Authentication required.", "authenticated": False}), 401
#     return wrapper

# @app.route("/api/", strict_slashes=False)
# def status():
#     try:
#         datasets = []
#         time_labels = []
#         xaxis_labels = []

#         offset = 1  # GMT+1 as Default Timezone offset
#         if request.headers.get('offset'):
#             offset = int(request.headers.get('offset'))
#         logger.debug("Timezone offset: %s" % offset)

#         return jsonify({'labels': xaxis_labels,
#                         'datasets': datasets,
#                         'time_labels': time_labels}), 200
#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         del exc_type
#         del exc_obj
#         logger.error('Error retrieving status (line %d): %s' % (exc_tb.tb_lineno, e))
#         return jsonify({'data': {}, 'error': 'Could not retrieve status, check logs for more details..'}), 500


# @app.route("/setup/password/", methods=['POST'], strict_slashes=False)
# @authenticated
# def set_password():
#     if request.method == 'POST':
#         data = ast.literal_eval(request.data)
#         if 'password' in data:
#             password = sanitize_user_input(data['password'])
#             if store_password(password):
#                 return jsonify({"data": {"response": "Success!"}}), 200
#             else:
#                 return jsonify({"data": {}, "error": "Could not set password"}), 500
#         else:
#             return jsonify({"data": {}, "error": "Password needs to be specified"}), 500
#     else:
#         return jsonify({"data": {}, "error": "Incorrect request method"}), 500

# @app.route("/auth/login/", methods=['POST'], strict_slashes=False)
# def login():
#     global config_file
#     if request.method == 'POST':
#         data = ast.literal_eval(request.data)
#         if 'password' in data and os.path.isfile(config_file):
#             config = ConfigParser.ConfigParser()
#             config.readfp(open(config_file))
#             if 'admin' in config.sections():
#                 current_password = config.get('admin', 'password')
#                 password = sanitize_user_input(data['password'])
#                 if obfuscate(password) == current_password:
#                     session.clear()
#                     session['admin_user'] = True
#                     return jsonify({"data": {"response": "Login success!", "authenticated": True}}), 200
#                 else:
#                     return jsonify({"data": {}, "error": "Unauthorised, authentication failure.."}), 401
#             else:
#                 return jsonify({'data': {}, 'error': 'Could not retrieve current credentials..'}), 500
#         else:
#             return jsonify({"data": {}, "error": "Password needs to be specified"}), 500
#     else:
#         return jsonify({"data": {}, "error": "Incorrect request method"}), 500


# @app.route("/auth/logout/", methods=['GET', 'POST'], strict_slashes=False)
# @authenticated
# def logout():
#     try:
#         session.clear()
#         return jsonify({"data": {"response": "Logged out successfully!"}}), 200
#     except Exception as e:
#         logger.error('Error while logging out: %s' % e)
#         return jsonify({'data': {}, 'error': 'Exception encountered while logging out..'}), 500


# def store_password(password):
#     global config_file
#     try:
#         config = ConfigParser.ConfigParser()
#         if os.path.isfile(config_file):
#             config.readfp(open(config_file))
#             if 'admin' in config.sections():
#                 config.remove_section('admin')
#         config.add_section('admin')
#         config.set('admin', 'password', obfuscate(password))

#         with open(config_file, 'w') as outfile:
#             config.write(outfile)

#         return True
#     except Exception:
#         return False

# Main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, use_reloader=False, debug=True)

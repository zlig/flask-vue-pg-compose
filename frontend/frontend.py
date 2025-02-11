#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Frontend service
#
import base64
import datetime
import logging
import os
import random
import configparser

from flask import Flask, render_template, send_from_directory, jsonify, request, session
from pydantic import ValidationError
from redis import Redis

from models import *

from functools import wraps
from codecs import encode
import secrets

# Global Config
local_path = os.path.dirname(os.path.abspath(__file__))
config_file = local_path+'/config/settings.cfg'
secret_file = local_path+'/config/secret.uti'
db_user = os.environ['POSTGRES_USER']
db_pass = os.environ['POSTGRES_PASSWORD']
db_host = "info-db"
db_port = "5432"
db_name = os.environ['POSTGRES_DB']
db_uri = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

# Loggingb
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('root')

# Application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# TODO check if can simplify loading config
#app.config.from_object(os.environ['APP_SETTINGS'])

# DB Session
db.init_app(app)

# Redis
redis = Redis(host='info-redis', port=6379)


# Errors Handlers
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404

@app.errorhandler(ValidationError)
def pydantic_validation_error(e):
    return jsonify({"data": "", "error": "invalid parameter value"}), 500

def sanitize_user_input(word):
    black_list = ['__import__', '/', '\\', '&', ';']
    for char in black_list:
        word = word.replace(char, '')
    return word

# Functions
def generate_string(length):
    import random
    import string
    result = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result

def generate_number(minimum=1, maximum=100):
    return random.randint(minimum, maximum)

def store_admin_password(password):
    global config_file
    try:
        config = configparser.ConfigParser()
        if os.path.isfile(config_file):
            config.readfp(open(config_file))
            if 'admin' in config.sections():
                config.remove_section('admin')
        config.add_section('admin')
        config.set('admin', 'password', obfuscate(password))

        with open(config_file, 'w') as outfile:
            config.write(outfile)

        return True
    except Exception:
        return False


# Authentication
def authenticated(func):
    """Checks whether user is logged in or raises error 401."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('username', False):
            return func(*args, **kwargs)
        else:
            return jsonify({"data": {}, "error": "Authentication required.", "authenticated": False}), 401
    return wrapper

def admin_required(func):
    """Custom decorator to check if the user has admin role"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('admin_user', False):
            return func(*args, **kwargs)
        else:
            return jsonify({"data": {}, "error": "You do not have sufficient privileges.", "authenticated": False}), 401
    return decorated_function

def generate_api_token():
    return secrets.token_urlsafe()

def obfuscate(text, decode=False):
    try:
        if decode:
            return base64.b64decode(decode(text, 'rot13'))
        else:
            return base64.b64encode(encode(text, 'rot13'))
    except Exception as e:
        logger.error('Error while encoding or decoding text: %s' % e)
        return text

@app.route("/auth/login/", methods=['POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return jsonify({"data": {}, 'error': 'Username and password are required'}), 400

            account = Account.query.filter_by(username=username).first()

            if account and check_password_hash(account.password_hash, password):
                session['authenticated'] = True
                session['username'] = username
                session['login_time'] = datetime.datetime.now() 
                return jsonify({"data": {"response": "Login successful", "authenticated": True}}), 200
            else:
                return jsonify({"data": {}, 'error': 'Invalid username or password'}), 401
        except Exception as e:
            logger.error('Error serving %s: %s' % (request.path, e))
            return jsonify({'data': {}, 'error': 'Could serve web application, check logs for more details..'}), 500

@app.route("/auth/logout/", methods=['GET', 'POST'], strict_slashes=False)
@authenticated
def logout():
    try:
        session.clear()
        return jsonify({"data": {"response": "Logged out successfully!"}}), 200
    except Exception as e:
        logger.error('Error while logging out: %s' % e)
        return jsonify({'data': {}, 'error': 'Exception encountered while logging out..'}), 500


# Routes
@app.route("/")
@app.route("/hello")
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/hi")
@app.route("/hi/<name>")
def hi(name=None):
    if name:
        return jsonify({"data": "hi, %s" % name}), 200
    else:
        return jsonify({"data": "hi"}), 200

@app.route("/ping")
def ping():
    logger.error('Ping session is: %s' % session)
    return jsonify({"response": "pong"}), 200

@app.route('/redis')
def hello():
    redis.incr('hits')
    views = int.from_bytes(redis.get('hits'))
    print('Redis views: %d' % views, flush=True)
    return jsonify({"data": str(views)}), 200

@app.route("/forbidden")
@authenticated
def hello_authenticated():
    return jsonify({"response": "hello authenticated user"}), 200


# Accounts

@app.route('/accounts', methods=['GET'], strict_slashes=False)
def get_accounts():
    accounts = db.session.query(Account).all()
    return jsonify({"data": [a.as_dict() for a in accounts]}), 200

@app.route('/accounts/<int:id>')
def get_account(id):
    account = db.session.get(Account, id)
    if account:
        return jsonify({"data": [account.as_dict()]}), 200
    else:
        return jsonify(), 204

@app.route('/accountmodel/<id>', methods=["GET"])
def get_account_by_querymodel(id):
    query = AccountQueryModel.model_validate({'account_id': id})
    account = db.session.get(Account, query.account_id)
    if account:
        response= AccountResponseModel.model_validate(account)
        return jsonify({"data": [response.model_dump()]}), 200
    else:
        return jsonify(), 204

@app.route('/accounts', methods=["POST"])
def add_account():
    try:
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        email = request.json['email']
        age = request.json['age']
        biography = request.json['biography']
        new_account = Account(firstname=firstname, lastname=lastname, email=email, age=age, biography=biography)

        db.session.add(new_account)
        db.session.commit()

        return jsonify({"response": "inserted account %d" % new_account.account_id}), 200

    except Exception as e:
        return jsonify({"data": {}, "error": "insertion failed"}), 500

@app.route('/accounts', methods=["DELETE"])
def delete_account():
    try:
        account_id = request.json['account_id']

        Account.query.filter(Account.account_id == account_id).delete()

        db.session.commit()

        return jsonify({"response": "deleted account %d" % account_id}), 200

    except Exception as e:
        return jsonify({"data": {}, "error": "deletion failed"}), 500


# Articles

@app.route('/articles', methods=['GET'], strict_slashes=False)
def get_articles():
    articles = db.session.query(Article).all()
    return jsonify({"data": [a.as_dict() for a in articles]}), 200

@app.route('/articles/<int:id>')
def get_article(id):
    article = db.session.get(Article, id)
    if article:
        return jsonify({"data": [article.as_dict()]}), 200
    else:
        return jsonify(), 204

@app.route('/articlemodel/<id>', methods=["GET"])
def get_article_by_querymodel(id):
    query = ArticleQueryModel.model_validate({'article_id': id})
    article = db.session.get(Article, query.article_id)
    if article:
        response= ArticleResponseModel.model_validate(article)
        return jsonify({"data": [response.model_dump()]}), 200
    else:
        return jsonify(), 204

@app.route('/articles', methods=["POST"])
def add_article():
    try:
        if 'account_id' in session:
            # TODO - Create article
            title = request.json['title']
            description = request.json['description']
            main = request.json['main']
            thumbnail = request.json['thumbnail']
            # TODO implement login
            account_id = session['account_id'] 
            new_article= Article(title=title, description=description, main=main, thumbnail=thumbnail, account_id=account_id)

            db.session.add(new_article)
            db.session.commit()
        else:
            return jsonify({"data": {}, "error": "unauthorized"}), 401

        return jsonify({"response": "inserted article %d" % new_article.article_id}), 200

    except Exception as e:
        return jsonify({"data": {}, "error": "insertion failed"}), 500

@app.route('/articles', methods=["DELETE"])
def delete_article():
    try:
        article_id = request.json['article_id']

        Article.query.filter(Article.article_id == article_id).delete()

        db.session.commit()

        return jsonify({"response": "deleted article %d" % article_id}), 200

    except Exception as e:
        return jsonify({"data": {}, "error": "deletion failed"}), 500

@app.route('/tests/data/accounts/')
def add_tests_data_accounts():
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

@app.route('/init')
def init():
    output = ""
    # Initialise database
    from sqlalchemy import create_engine
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


@app.route('/urlmap')
def get_url_map():
    return ['%s' % rule for rule in app.url_map.iter_rules()]


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

# Main
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, use_reloader=False, debug=True)

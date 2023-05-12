#!/usr/bin/env python
import os

from flask import Flask, render_template, jsonify, request, url_for, redirect
import json
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
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Account {self.firstname}>'


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
    johndoe = Account(firstname='john', lastname='doe',
                       email='jd@example.com', age=79,
                       bio='Simple user')
    return jsonify({"data": str(johndoe.id)}), 200

@app.route('/init')
def init():
    # Initialise database
    from sqlalchemy_utils import database_exists, create_database
    engine = create_engine(db_uri)
    if not database_exists(engine.url):
        print("Database does not exist, creating")
        create_database(engine.url)
    try:
       db.drop_all()
    except OperationalError:
       pass
    db.create_all()
    return jsonify({"data": "All tables created."}), 200

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, use_reloader=False, debug=True)

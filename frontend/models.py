from datetime import datetime
from pydantic import BaseModel, EmailStr
# from email_validator import validate_email, EmailNotValidError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func

from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Models
class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    biography = db.Column(db.Text)
    # Define a one-to-one relationship with Password Hashes
    password_hash = db.relationship('PasswordHash', uselist=False, backref='account', lazy=True)
    # Define a one-to-one relationship with API tokens
    api_token = db.relationship('APIToken', uselist=False, backref='account', lazy=True)

    def set_password(self, secret):
        self.password = generate_password_hash(secret)

    def check_password(self, secret):
        return check_password_hash(self.password, secret)

    def __repr__(self):
        return f'<Account {self.firstname} {self.lastname} {self.email}>'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class AccountModel(BaseModel):
    account_id: int
    firstname: str
    lastname: str
    email: EmailStr
    # password: SecretStr
    age: int
    created_at: datetime
    email: str
    biography: str

class AccountResponseModel(BaseModel):
    firstname: str
    lastname: str
    email: str
    age: int
    created_at: datetime
    email: EmailStr
    biography: str
    class Config:
       from_attributes = True

class AccountQueryModel(BaseModel):
    account_id: int


class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    main = db.Column(db.Text, nullable=True)
    thumbnail = db.Column(db.String(2048), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    last_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())
    account_id = db.Column(db.Integer, db.ForeignKey('Account.account_id'))

    def __repr__(self):
        return f'<Article {self.name} {self.description}>'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ArticleModel(BaseModel):
    article_id: int
    title: str
    description: str
    main: str
    thumbnail: str
    account_id: int

class ArticleResponseModel(BaseModel):
    article_id: int
    title: str
    description: str
    main: str
    thumbnail: str
    account_id: int
    class Config:
       from_attributes = True

class ArticleQueryModel(BaseModel):
    article_id: int


class PasswordHash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(255), unique=True, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)

    # Define a backreference to the Account model
    account = db.relationship('Account', backref=db.backref('password_hash', uselist=False))

class APIToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)

    # Define a backreference to the Account model
    account = db.relationship('Account', backref=db.backref('api_token', uselist=False))
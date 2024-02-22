from datetime import datetime
from pydantic import BaseModel, EmailStr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func

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

    def __repr__(self):
        return f'<Account {self.firstname} {self.lastname} {self.email}>'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# class AccountSchema(BaseModel):
    # account_id: int
    # firstname: str = 'Jane'
    # lastname: str = 'Doe'
    # email: str = 'Jane@Doe.com'
    # age: int
    # created_at: datetime = None
    # email: str = 'Jane Doe'
    # biography: str = 'Jane@Doe.com'

class AccountResponseModel(BaseModel):
    firstname: str
    lastname: str
    email: str
    age: int
    created_at: datetime
    email: EmailStr
    biography: str

class AccountQueryModel(BaseModel):
    firstname: str
    lastname: str

class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    last_update = db.Column(db.DateTime(timezone=True), server_default=func.now())
    account_id = db.Column(db.Integer, db.ForeignKey('Account.account_id'))

    def __repr__(self):
        return f'<Article {self.name} {self.description}>'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

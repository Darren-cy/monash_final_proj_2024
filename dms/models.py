from . import db
from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
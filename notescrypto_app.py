import os
import random
from cryptography.fernet import Fernet
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sslify import SSLify
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
"""from werkzeug.contrib.fixers import ProxyFix
"""


class Config():
    # Configuration class for Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SITE_URL = 'https://notescrypto.herokuapp.com


# Object of Flask-class with settings of Config-class
app = Flask(__name__)
app.config.from_object(Config)

# Objects for db, migrate and ect.
db = SQLAlchemy(app)

migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
sslify = SSLify(app)


class Note(db.Model):
    # Model for DB
    __tabllename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True) # identifier for record in table
    number = db.Column(db.Integer, unique=True, nullable=False) # random generated number of record
    cryptotext = db.Column(db.Text, nullable=False) # encrypted not empty text

    def __repr__(self):
        return  f'<Note number: {self.number}'


class TextForm(FlaskForm):
    text = TextAreaField('Input text-message (max length = 10 000)',
                         validators=[DataRequired(), Length(1, 10000)])
    submit = SubmitField('Create')
# Register function in the shell context.
# This makes it possible to work with database objects without importing them every time
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Note': Note}

#route handlers


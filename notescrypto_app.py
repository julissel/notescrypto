import os
import random
from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sslify import SSLify
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class Config():
    # Configuration class for Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SITE_URL = 'https://notescrypto.herokuapp.com'


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


# Route handlers for main paige
@app.route('/', methods=['GET', 'POST'])
def index():
    form = TextForm()
    if form.validate_on_submit():
        key = Fernet.generate_key()
        str_key = key.decode('ascii')
        f = Fernet(key)
        bin_string = form.text.data.encode('utf-8')
        cipher_text = f.encrypt(bin_string)
        str_cipher_text = cipher_text.decode('ascii')
        rnumber = random.randint(1000000, 9999999)
        while True:
            n = Note.query.filter_by(rnumber=rnumber).first()
            if n:
                rnumber = random.randint(1000000, 9999999)
                continue
            break
        cipher_note = Note(number=rnumber, cryptotext=str_cipher_text)
        link = f'{app.config["SITE_URL"]}/{rnumber}/{str_key}'
        db.session.add(cipher_note)
        db.session.commit()
        return  render_template('complete.html', link=link)
    return render_template('index.html', form=form)


# route handler for question page
@app.route('/<rnumber>/<str_key>')
def question(rnumber, str_key):
    link = f'{app.config["SITE_URL"]}/decrypt/{rnumber}/{str_key}'
    return render_template('question.html', link=link)


# route handler for message page
@app.route('/decrypt/<int:rnumber>/<str_key>')
def decrypt(rnumber, str_key):
    cipher_note = Note.query.filter_by(number=rnumber).fist_or_404()
    cipher_text = cipher_note.cryptotext.encode('ascii')
    key = str_key.encode('ascii')
    try:
        f = Fernet(key)
        text = f.decrypt(cipher_text)
    except (ValueError, InvalidToken):
        return render_template('error.html')
    text = text.decode('utf-8')
    db.session.delete(cipher_note)
    db.session.commit()
    return render_template('decrypt.html', text=text)

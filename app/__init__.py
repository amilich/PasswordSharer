#!flask/bin/python

from flask import Flask
from flask.ext.mandrill import Mandrill
from forms import loginform
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin,
                            confirm_login, fresh_login_required)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import models

# login config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

# Mandrill config
app.config['MANDRILL_API_KEY'] = 'AlGPWLcyBN97zbLs59HcKw'
app.config['MANDRILL_DEFAULT_FROM'] = 'noreply@passwordsharer.com'
mandrill = Mandrill(app)

# we need a better secret key 
app.config['SECRET_KEY'] = '123456790'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

#!flask/bin/python

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators, PasswordField

class loginform(Form):
	email = StringField('Email', [validators.Required()])
	password = PasswordField('Password', [validators.Required()])
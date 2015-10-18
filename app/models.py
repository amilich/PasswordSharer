#!flask/bin/python
from app import db
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin,
                            confirm_login, fresh_login_required)

class User(db.Model, UserMixin):
	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(64), unique=False)

	def __init__(self, email, password, active=True):
		self.email = email
		self.password = password
		self.active = active
	def is_active(self):
		# make sure user's email is confirmed basically
		return self.active
	def is_anonymous(self):
		return False
	def is_authenticated(self):
		# this assumes you are already logged in, so this should be true
		return True
	def __repr__(self):
		return '<User %r>' % (self.email)

class Service(db.Model):
	service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(64), unique=False)
	owner = db.Column(db.String(120), db.ForeignKey('user.user_id')) # FK to user_id

class Group(db.Model):
	group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(120))
	group_hash = db.Column(db.String(5))

class GroupMembership(db.Model):
	membership_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	groupid = db.Column(db.Integer, db.ForeignKey('group.group_id')) # FK to group_id 
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id')) # FK to user_id

class ServiceMembership(db.Model):
	servicemembership_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	service_id = db.Column(db.Integer, db.ForeignKey('service.service_id')) # FK to service_id
	group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))
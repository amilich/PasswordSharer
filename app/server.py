from flask import Flask, Markup, session, Response, render_template, request, flash
from app import app, login_manager, mandrill
from models import *
from forms import loginform
import string, random

def hashgen(size=5, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def get_services():
	my_groups = get_groups()
	my_service_ids = models.ServiceMembership.query.join(my_groups, group_id=GroupMembership.group_id)
	my_services = models.Service.join(my_service_ids, service_id=ServiceMembership.group_id)
	return my_services

def get_groups():
	user_groups = []
	my_group_ids = models.GroupMembership.query.filter_by(user_id=current_user.user_id)
	my_groups = models.Group.query.join(my_groups, group_id=GroupMembership.group_id)
	return my_groups 

"""
	Creates a service and adds it to group. 
"""
def create_service(): 
	service_name = request.form['serviecname']
	service_password = request.form['service_password']
	owner_id = current_user.user_id 

	s = models.Group(name=service_name, service_password=service_password, owner=owner_id)
	db.session.add(g)
	db.session.commit()
	return

"""
	Add service to group. 
"""
def add_service_to_group():
	service_id = request.form['serviceid'] # should be hidden in the form
	group_id = request.form['groupid']
	add = models.Group(service_id=service_id, group_id=group_id)
	db.sessionadd(add)
	db.session.commit() 
	return 

"""
	Adds a group. 
"""
def create_group():
	group_name = request.form['groupname']
	group_hash = hashgen(5)
	
	g = models.Group(name=group_name, grouphash=group_hash)
	db.session.add(g)
	db.session.commit()
	return

"""
	Adds a user to the system. 
"""
def add_user(): 
	email = request.form['email']
	password = request.form['password']
	u = models.User(email=email, password=password)
	db.session.add(u)
	db.session.commit()
	return

@login_manager.user_loader
def load_user(id):
	# database???
    return USERS.get(int(id))

@app.route('/logout')
def logout():
	logout_user()
	# need return home template
	return render_template('index.html')

@app.route("/login", methods=["GET","POST"])
def login():
	form = loginform()

	# email = request['email']
	# password = request['password']

	if form.validate_on_submit(): 
		email = form.email.data
		password = form.password.data
		for userid,user in USERS.iteritems(): 
			if email == user.email and password == user.password: 
				print 'in'
				if(login_user(user)):
					print 'logged in'
					return "YOU ARE LOGGED IN"
				else: 
					return "LOGIN FAILED"
		return "INVALID"
	return render_template("login.html", form=form)

@app.route("/",methods=["GET"])
def index():
    return "hi"

@app.route("/testmail")
def testmail():
	mandrill.send_email(
    from_email='noreply@passwordsharer.com',
    subject='Your invite to PasswordSharer',
    to=[{'email': 'useremail@useremail.com'}],
    text=Markup('Your invite to password sharer'))

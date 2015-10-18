from flask import Flask, Markup, session, Response, render_template, request, flash
from app import app, login_manager, mandrill
from models import *
from forms import loginform
import string, random

USERS = {
    1: User("a@a.com", 'a', 1),
    2: User("b@b.com", 'b', 2),
    3: User("c@c.com", 'c', 3),
}

def hashgen(size=5, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

"""
	Adds a group. 
"""
def add_group():
	name = request.form['servicename']
	grouphash = hashgen(5)
	g =  models.Group(name=name, grouphash=grouphash)
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

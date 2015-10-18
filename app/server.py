from flask import Flask, Markup, session, Response, render_template, request, flash
from app import app, login_manager, mandrill
from models import *
from forms import loginform

USERS = {
    1: User("a@a.com", 'a', 1),
    2: User("b@b.com", 'b', 2),
    3: User("c@c.com", 'c', 3),
}

def add_user(): 
	return

@app.route("/protected/",methods=["GET"])
@login_required
def protected():
    return Response(response="Hello Protected World!", status=200)

@login_manager.user_loader
def load_user(id):
	# database???
    return USERS.get(int(id))

@app.route('/logout')
def logout():
	print 'hi2'
	logout_user()
	return 'logged out'

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


@app.route("/add_to_group",methods=["POST"])
def add_to_group():
    form = loginform()
    user_table = Table('User', metadata, autoload=True)
    if form.validate_on_submit(): 
        emails = form.emails.data
        group_id = form.group_id.data
        for email in emails:
        	invite_to_group(email, group_id)
            

def invite_to_group(email, group_id):
	if hasAccount(email):
    	send_group_invite_email(email, group_id)
    else:
    	send_signup_email(email, group_id)


def has_account(email, user_table):
	user = user_table.select(user_table.c.email == email).execute().first()
	if user:
		return True;
	else:
		return False


def send_group_invite_email(email):
	print 'send_group_invite_email'


def send_signup_email(email):
	print 'send_group_invite_email'


@app.route("/testmail")
def testmail():
	mandrill.send_email(
    from_email='noreply@passwordsharer.com',
    subject='Your invite to PasswordSharer',
    to=[{'email': 'useremail@useremail.com'}],
    text=Markup('Your invite to password sharer'))

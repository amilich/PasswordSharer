from flask import Flask, Markup, session, Response, render_template, request, flash
from flask.ext.mandrill import Mandrill
from forms import loginform
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin,
                            confirm_login, fresh_login_required)

app = Flask(__name__)

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


class User(UserMixin):
    def __init__(self, email, password, userid, active=True):
        self.email = email
        self.id = userid
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

USERS = {
    1: User("a@a.com", 'a', 1),
    2: User("b@b.com", 'b', 2),
    3: User("c@c.com", 'c', 3),
}

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

@app.route("/testmail")
def testmail():
	mandrill.send_email(
    from_email='noreply@passwordsharer.com',
    subject='Your invite to PasswordSharer',
    to=[{'email': 'useremail@useremail.com'}],
    text=Markup('Your invite to password sharer'))

if __name__ == "__main__":
    app.run(debug=True)

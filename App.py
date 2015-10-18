from flask import Flask, Markup, session, Response, render_template, request, flash
from flask.ext.mandrill import Mandrill
from forms import loginform
from flask.ext.mysql import MySQL
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)

app = Flask(__name__)

# login config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

# Mandrill config
app.config['MANDRILL_API_KEY'] = 'AlGPWLcyBN97zbLs59HcKw'
app.config['MANDRILL_DEFAULT_FROM'] = 'noreply@passwordsharer.com'
mandrill = Mandrill(app)

# we need a better secret key 
app.config['SECRET_KEY'] = '123456790'


mysql = MySQL() 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'psdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
data = cursor.fetchall()
 
if len(data) is 0:
    conn.commit()
    return json.dumps({'message':'User created successfully !'})
else:
    return json.dumps({'error':str(data[0])})


user_database = {1: ("JohnDoe@johnthebomb.com", "John", 1),
               2: ("Jane@aol.com", "Jane", 2)} # temporary database

USERS = {
    1: User(u"Andrew", 1),
    2: User(u"Bob", 2),
    3: User(u"Rob", 3, False),
}
USER_NAMES = dict((u.name, u) for u in USERS.itervalues())


class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        # make sure user's email is confirmed basically
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
    	# this assumes you are already logged in, so this should be true
        return True

@login_manager.user_loader
def load_user(id):
	# database???
    return USERS.get(int(id))

@app.route("/login", methods=["GET","POST"])
def login():
	form = loginform()
    if form.validate_on_submit():
    	email = form.email.data
    	password = form.password.data
    	if username in USER_NAMES: 
    		if(login_user(USER_NAMES[username])):
    			flash("logged in!")
    		else: 
    			flash("login failed. sorry!")
    	else: 
    		flash("Invalid login.")
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

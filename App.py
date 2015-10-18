from flask import Flask, Markup, session, Response, render_template, request
from flask.ext.mandrill import Mandrill
from flask.ext.login import LoginManager, UserMixin, login_required
from forms import loginform
from flask.ext.mysql import MySQL

app = Flask(__name__)

# login config
login_manager = LoginManager()
login_manager.init_app(app)

# Mandrill config
app.config['MANDRILL_API_KEY'] = 'AlGPWLcyBN97zbLs59HcKw'
app.config['MANDRILL_DEFAULT_FROM'] = 'noreply@passwordsharer.com'
mandrill = Mandrill(app)

# we need a better secret key 
app.config['SECRET_KEY'] = '123456790'

# database config
# app.config['DATABASE_FILE'] = 'sample_db.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
# app.config['SQLALCHEMY_ECHO'] = True
# db = SQLAlchemy(app)

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

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        	# Andrew: ie email confirmed
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

@login_manager.user_loader
def load_user(id):
    # 1. Fetch against the database a user by `id` 
    # 2. Create a new object of `User` class and return it.
    # ultimately: u = DBUsers.query.get(id)
    return User(u.name,u.id,u.active)

@app.route("/login", methods=["GET","POST"])
def login():
	form = loginform()
    if form.validate_on_submit():
        # do something
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

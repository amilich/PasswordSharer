from flask import Flask, Markup, session
from flask.ext.mandrill import Mandrill

app = Flask(__name__)
app.config['MANDRILL_API_KEY'] = 'AlGPWLcyBN97zbLs59HcKw'
app.config['MANDRILL_DEFAULT_FROM'] = 'noreply@passwordsharer.com'
mandrill = Mandrill(app)

@app.route("/testmail")
def testmail():
	mandrill.send_email(
    from_email='noreply@passwordsharer.com',
    subject='Your invite to PasswordSharer',
    to=[{'email': 'useremail@useremail.com'}],
    text=Markup('Your invite to password sharer'))

@app.route("/hello")
def hello():
    return "Andrew!"

@app.route("/")
def slash():
	return "Hello"
	return render_template("static/login.html")

if __name__ == "__main__":
    app.run()
    app.debug = True

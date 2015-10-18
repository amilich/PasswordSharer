from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Andrew!"

if __name__ == "__main__":
    app.run()

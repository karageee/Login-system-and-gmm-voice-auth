from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/user.db'
db = SQLAlchemy(app)

class UsersModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), nullable = False)
    password = db.Column(db.String(25), nullable = False)
    fullname = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f"UsersModel(username={username}, password={password}, fullname={fullname})"

db.create_all()

@app.route("/")
def login():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, session, redirect
from functools import wraps
from flask_cors import CORS
import pymongo

app = Flask(__name__)
CORS(app)
app.secret_key = 'e91e518a-4400-4a33-8f36-eb9e5ccdb096'

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.Login

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  return wrap

def Authentication_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'authenticated' in session and 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/voice_signin/')
  return wrap

# Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@Authentication_required
def dashboard():
  return render_template('dashboard.html')

@app.route('/voice_signup/')
@login_required
def voice_signup():
  return render_template('voice_signup.html')

@app.route('/voice_signin/')
@login_required
def voice_signin():
  return render_template('voice_signin.html')

if __name__ == '__main__':
  app.run(port=5000, debug=True)
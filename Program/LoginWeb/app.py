from flask import Flask, render_template, session, redirect
from functools import wraps
from flask_cors import CORS
from flask_cors.decorator import cross_origin
import pymongo

app = Flask(__name__)
CORS(app)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

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

# Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')

@app.route('/voice_signup/')
def voice():
  return render_template('voice_signup.html')

if __name__ == '__main__':
  app.run(port=5000, debug=True)
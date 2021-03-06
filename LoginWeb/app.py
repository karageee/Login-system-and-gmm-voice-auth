from flask import Flask, render_template, session, redirect, request, render_template_string
from functools import wraps
import pymongo

app = Flask(__name__)
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
    if session['authenticated'] == True:
      return f(*args, **kwargs)
    else:
      return redirect('/voice_signin/')
  return wrap

# Routes
from user import routes

@app.errorhandler(404)
def page_not_found(e):
  template = '''
  <div class="center-content error">
  <h1>Oops! That page doesn't exist.</h1>
  <h3>%s</h3>
  </div>
  ''' % (request.url)

  return render_template_string(template), 404

@app.route('/')
def home():
  return render_template('home.jinja2')

@app.route('/dashboard/')
@login_required
@Authentication_required
def dashboard():
  return render_template('dashboard.jinja2')

@app.route('/voice_signup/')
@login_required
def voice_signup():
  return render_template('voice_signup.jinja2')

@app.route('/voice_signin/')
@login_required
def voice_signin():
  return render_template('voice_signin.jinja2')

if __name__ == '__main__':
  app.run(host='localhost', port=5000, debug=True)
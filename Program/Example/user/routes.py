from flask import Flask, request, render_template
from app import app
from user.models import User

@app.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/user/signout')
def signout():
  return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
  return User().login()

@app.route('/test', methods=['POST','GET'])
def voice():
  if request.method == "POST":
    f = request.files['audio_data']
    with open('audio.wav', 'wb') as audio:
      f.save(audio) 
    print('file uploaded successfully')
    return render_template('voice_signup.html', request="POST")
  else:
    return render_template("voice_signup.html")
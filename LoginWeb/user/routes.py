from flask import Flask
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

@app.route('/user/voice_signup', methods=['POST'])
def voice_register():
  return User().voice_signup()

@app.route('/user/voice_signin', methods=['POST'])
def voice_login():
  return User().voice_signin()
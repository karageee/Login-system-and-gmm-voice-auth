from flask import Flask, jsonify, request, session, redirect
from passlib.hash import md5_crypt
from app import db
import uuid

base = "http://192.168.100.22:5000/"

class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    print(request.form)

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password')
    }

    # Encrypt the password
    user['password'] = md5_crypt.encrypt(user['password'])

    # Check for existing email address
    if db.Users.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.Users.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    user = db.Users.find_one({
      "email": request.form.get('email')
    })

    if user and md5_crypt.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401

  def voice_signup(self):
    if(session != null):
      user = db.Users.find_one({
        "email": session['user']
      })
      response = request.post(base + "voice_add/" + user, request.form.get('voice'))
      return response


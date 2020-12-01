from flask import Flask, jsonify, request, session, redirect, send_from_directory
from passlib.hash import md5_crypt
from app import db
import uuid
import requests
import os
import json
class User:
  base = "http://127.0.0.1:5001/"

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['authenticated'] = False
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
      self.start_session(user)
      user_id={
        "user_id": user['_id']
      }
      response = requests.post(self.base + "user/", data = user_id)
      return response.json()

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
    user = session['user']
    for i in range(3):
      f = request.files['voice'+str((i+1))]
      f.save(os.path.join("./user/Temp", f.filename))
      a = open("./user/Temp/"+f.filename, 'rb')

      dataObj={}
      dataObj['user_id']=user
      filesObj = [('voice', (f.filename, a, 'audio/wav'))]
      response = requests.post(self.base + "voice_add/", data = dataObj, files = filesObj)

      os.remove("./user/Temp/"+f.filename)

      x = json.loads(response)
      if (x["category"] == "success") and (f.filename == "3.wav"):
        session['authenticated'] = True
      if x["status" != 200]:
        return jsonify({"error": x["message"]})
    return redirect("/dashboard/")

  def voice_signin(self):
    user = session['user']
    f = request.files['voice']
    f.save(os.path.join("./user/Temp", f.filename))
    a = open("./user/Temp/"+f.filename, 'rb')

    dataObj={}
    dataObj['user_id']=user
    filesObj = [('voice', (f.filename, a, 'audio/wav'))]
    response = request.post(self.base + "voice_recog/", data = dataObj, files = filesObj)

    os.remove("./user/Temp/"+f.filename)
    x = json.loads(response)
    if(x["message"] == user):
      session['authenticated'] = True
    if x["status" != 200]:
        return jsonify({"error": x["message"]})
    return redirect("/dashboard/")

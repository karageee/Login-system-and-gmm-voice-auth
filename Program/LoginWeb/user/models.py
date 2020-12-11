from datetime import timedelta
from flask import Flask, jsonify, request, session, redirect
from passlib.hash import md5_crypt
from werkzeug.datastructures import Headers
from app import db, app
from datetime import datetime
import uuid
import requests
import os
import json
import jwt

class User:
  base = "http://127.0.0.1:5001/"
  api_key = "144cc764-0878-4484-9a36-ada1128fb3ae"

  def jwt_encode(self):
    token = jwt.encode({'app_id': app.secret_key, 'exp':datetime.utcnow() + timedelta(seconds=0.1)}, self.api_key)
    print(str(token.decode('UTF-8')))
    headersdata = {}
    headersdata['x-access-token'] = str(token.decode('UTF-8'))
    return headersdata

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
      response = requests.post(self.base + "user/", data = user_id, headers=self.jwt_encode())
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
    user = session['user']["_id"]
    for i in range(3):
      f = request.files['voice'+str((i+1))]
      f.save(os.path.join("./user/Temp", f.filename))
      a = open("./user/Temp/"+f.filename, 'rb')

      print(f.filename)

      dataObj={}
      dataObj['user_id']=user
      filesObj = [('voice', (f.filename, a, 'audio/wav'))]

      response = requests.post(self.base + "voice_add/", data = dataObj, files = filesObj, headers=self.jwt_encode)

      a.close()

      os.remove("./user/Temp/"+f.filename)

      print(response.json())
      x = json.loads(response.json())
      if (x["category"] == "success") and (f.filename == "3.wav"):
        session['authenticated'] = True
        return redirect("/dashboard/")
      if x["status"] != 200:
        return jsonify({"error": x["message"]})

  def voice_signin(self):
    user = session['user']["_id"]
    f = request.files['voice']
    f.save(os.path.join("./user/Temp", f.filename))
    a = open("./user/Temp/"+f.filename, 'rb')

    dataObj={}
    dataObj['user_id']=user
    filesObj = [('voice', (f.filename, a, 'audio/wav'))]

    check_voice_exist = requests.get(self.base + "user/", data = dataObj, headers = self.jwt_encode())
    result = check_voice_exist.json()
    if(result['status'] == 404):
      a.close()
      os.remove("./user/Temp/"+f.filename)
      return redirect("/voice_signup/")
    elif (result['status'] == 200):
      response = requests.post(self.base + "voice_recog/", data = dataObj, files = filesObj, headers=self.jwt_encode())

      a.close()
      os.remove("./user/Temp/"+f.filename)
    
      x = response.json()
      print (user)
      print (x)
      if x['message'] == user:
        session['authenticated'] = True
        return redirect("/dashboard/")
      if x['status'] != 200:
        return jsonify({"error": x['message']})



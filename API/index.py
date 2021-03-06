from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort, marshal_with, reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app import voices
from functools import wraps
import os
import jwt
import random

app = Flask("__name__")
CORS(app)
api = Api(app)
app.config['SECRET_KEY'] = '144cc764-0878-4484-9a36-ada1128fb3ae'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user/database.db'
db = SQLAlchemy(app)
parent_dir = "./app/voice_database"

class UsersModel(db.Model):
    auth_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    voice_loc = db.Column(db.String(300), nullable=False)
    def __repr__(self):
        return f"Users(user_id = {user_id}, voice_loc = {voice_loc})"

# db.create_all()

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("user_id", type=str, help="User's UserID is required", required=True)
user_get_args = reqparse.RequestParser()
user_get_args.add_argument("user_id", type=str, help="User's UserID is required", required=True)

user_fields = {
    'auth_id' : fields.String,
    'user_id' : fields.String,
    'voice_loc' : fields.String
}

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # jwt is passed in the request header 
        if 'x-access-token' in request.headers: 
            token = request.headers['x-access-token']
        # return 401 if token is not passed 
        if not token: 
            return jsonify(message='Token is missing !!', status=401)
        try: 
            # decoding the payload to fetch the stored details 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            if data['app_id'] != 'e91e518a-4400-4a33-8f36-eb9e5ccdb096':
                return jsonify(message = 'Invalid credentials', status=401)
            print(data)
        except: 
            return jsonify(message = 'Token is invalid !!', status=401)
        return f(*args, **kwargs)
    return decorator

class Users(Resource):
    @token_required
    def get(self):
        args = user_get_args.parse_args()
        print(args['user_id'])
        query = UsersModel.query.filter_by(user_id=args['user_id']).first()
        if not query:
            return jsonify(message="Cannot find user id", status=404)
        if os.path.isfile(query.voice_loc + "/1.wav"):
            return jsonify(message="voice found", status=200)
        else:
            return jsonify(message="There's no voice yet", status=404)

    @marshal_with(user_fields)
    @token_required
    def post(self):
        args = user_post_args.parse_args()
        response = UsersModel.query.filter_by(user_id=args['user_id']).first()
        if response:
            abort (409, message="User id taken...")

        path = os.path.join(parent_dir, args['user_id'])
        os.mkdir(path)
        i = UsersModel.query.count()
        user = UsersModel(auth_id=i, user_id=args['user_id'], voice_loc=path)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="user created", status=201)

class Voice_add(Resource):
    @token_required
    def post(self):
        path = os.path.join(parent_dir, request.form['user_id'])
        if 'voice' not in request.files:
            return 'no voice found'  
        file = request.files['voice']
        if file.filename == '':
            abort (400, message="No file selected for uploading")
        
        file.save(os.path.join(path, file.filename))
        if file.filename == "3.wav":
            voices.add_user(request.form['user_id'])
        return jsonify(message= "file successfully added", category= "success", status=200)

class Voice_recog(Resource):
    @token_required
    def post(self):
        path = os.path.join(parent_dir, request.form['user_id'])
        print(request.form.getlist)
        if 'voice' not in request.files:
            return 'no voice found'  
        file = request.files['voice']
        if file.filename == '':
            abort (400, message="No file selected for uploading")
        msg = voices.recognize(request.form['user_id'], (os.path.join(path, file.filename)))
        if msg == True:
            query = UsersModel.query.filter_by(user_id=request.form['user_id']).first()
            for i in os.listdir(query.voice_loc):
                number = int(i.split(".wav")[0])
            file.save(os.path.join(path, (str(number + 1))+".wav"))
            if((number+1)%3 == 0):
                voices.add_user(request.form['user_id'])
            voices.add_user(request.form['user_id'])
        print (msg)
        return jsonify(message= msg, category="success", status=200)

api.add_resource(Users, "/user/")
api.add_resource(Voice_add, "/voice_add/")
api.add_resource(Voice_recog, "/voice_recog/")

if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)

from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort, marshal_with, reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from app import voices
import os

app = Flask("__name__")
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user/database.db'
db = SQLAlchemy(app)
parent_dir = "./app/voice_database"

class UsersModel(db.Model):
    auth_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    voice_loc = db.Column(db.String(300), nullable=False)
    def __repr__(self):
        return f"Users(user_id = {user_id}, voice_loc = {voice_loc})"

db.create_all()

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("user_id", type=str, help="User's UserID is required", required=True)

user_fields = {
    'auth_id' : fields.Integer,
    'user_id' : fields.String,
    'voice_loc' : fields.String
}

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        response = UsersModel.query.all()
        if not response:
            abort(404, message="Cannot find user id")
        return response

    @marshal_with(user_fields)
    def post(self):
        args = user_post_args.parse_args()
        response = UsersModel.query.filter_by(user_id=args['user_id']).first()
        if response:
            abort(409, message="User id taken...")

        path = os.path.join(parent_dir, args['user_id'])
        os.mkdir(path)
        i = UsersModel.query.count()
        user = UsersModel(auth_id=i, user_id=args['user_id'], voice_loc=path)
        db.session.add(user)
        db.session.commit()

        return user, 201

class Voice_add(Resource):
    def post(self, user_id):
        path = os.path.join(parent_dir, user_id)
        if 'voice' not in request.files:
            return 'no voice found'  
        file = request.files['voice']
        if file.filename == '':
            abort (400, message="No file selected for uploading")
        
        file.save(os.path.join(path, file.filename))
        voices.add_user(user_id)
        return jsonify(message= "file successfully added", category= "success", status=200)

class Voice_recog(Resource):
    def post(self, user_id):
        path = os.path.join(parent_dir, user_id)
        print(request.form.getlist)
        if 'voice' not in request.files:
            return 'no voice found'  
        file = request.files['voice']
        if file.filename == '':
            abort (400, message="No file selected for uploading")
        file.save(os.path.join(path, file.filename))
        return jsonify(message= (voices.recognize(user_id, (os.path.join(path, file.filename)))), category="success", status=200)

api.add_resource(Users, "/user/")
api.add_resource(Voice_add, "/voice_add/<string:user_id>")
api.add_resource(Voice_recog, "/voice_recog/<string:user_id>")

if __name__ == "__main__":
    app.run(host='192.168.100.22', port=5001, debug=True)

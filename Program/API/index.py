from flask import Flask
from flask_restful import Api, Resource, abort, marshal_with, reqparse, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__")
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user/database.db'
db = SQLAlchemy(app)

class UsersModel(db.Model):
    auth_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    voice_loc = db.Column(db.String(300), nullable=False)
    def __repr__(self):
        return f"Users(user_id = {user_id}, voice_loc = {voice_loc})"

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("user_id", type=str, help="User's UserID is required", required=True)
user_post_args.add_argument("voice_loc", type=str, help="User's voice location is required", required=True)

resource_fields = {
    'auth_id' : fields.Integer,
    'user_id' : fields.String,
    'voice_loc' : fields.String
}

class Users(Resource):
    @marshal_with(resource_fields)
    def get(self):
        response = UsersModel.query.all()
        if not response:
            abort(404, message="Cannot find user id")
        return response

    @marshal_with(resource_fields)
    def post(self):
        args = user_post_args.parse_args()
        response = UsersModel.query.filter_by(user_id=args['user_id']).first()
        if response:
            abort(409, message="User id taken...")

        i = UsersModel.query.count()
        user = UsersModel(auth_id=i, user_id=args['user_id'], voice_loc=args['voice_loc'])
        db.session.add(user)
        db.session.commit()
        return user, 201


api.add_resource(Users, "/user/")

if __name__ == "__main__":
    app.run(debug=True)
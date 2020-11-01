from flask import Flask
from flask_restful import Api, Resource, marshal_with, reqparse, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__")
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user/database.db'
db = SQLAlchemy(app)

class UsersModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    voice_loc = db.Column(db.String(300), nullable=False)
    def __repr__(self):
        return f"Users(user_id = {user_id}, voice_loc = {voice_loc})"

db.create_all()

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("user_id", type=str, help="User's UserID is required", required=True)
user_put_args.add_argument("voice_loc", type=str, help="User's voice location is required", required=True)

resource_fields = {
    'id' : fields.Integer,
    'user_id' : fields.String,
    'voice_loc' : fields.String
}

class Users(Resource):
    @marshal_with(resource_fields)
    def get(self, userid):
        response = UsersModel.query.get(id=userid)
        return response

    @marshal_with(resource_fields)
    def put(self, userid):
        args = user_put_args.parse_args()
        user = UsersModel(id=userid, user_id=args['user_id'], voice_loc=args['voice_loc'])
        db.session.add(user)
        db.session.commit()
        return user, 201

api.add_resource(Users, "/user/<int:userid>")

if __name__ == "__main__":
    app.run(debug=True)

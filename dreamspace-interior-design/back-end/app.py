# backend/app.py
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)  # Enable CORS for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456'  # Change this to a secure secret key
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class UserResource(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        with app.app_context():
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

        return jsonify(message='User registered successfully'), 201

api.add_resource(UserResource, '/register')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

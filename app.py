from flask import Flask, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_caching import Cache
import time
from config import BaseConfig
from functools import wraps
import sqlite3
from datetime import timedelta
import requests

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from sqlalchemy import create_engine, Column, Integer, String, orm
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
app.config.from_object(BaseConfig)
cache = Cache(app)  # Initialize Cache

engine = create_engine('sqlite:///users.db')
db_session = scoped_session(sessionmaker(bind=engine))
Base = orm.declarative_base()


# User model
class User(Base):
    __tablename__ = 'users'

    name = Column(String(120))
    email = Column(String(120), primary_key=True)
    password_hash = Column(String(128))
    role = Column(String(10))

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password).decode('utf-8')
        self.role = role

    def save(self):
        db_session.add(self)
        db_session.commit()

    @staticmethod
    def find_by_email(email):
        return db_session.query(User).filter_by(email=email).first()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


Base.metadata.create_all(bind=engine)


# Example role-based authorization decorator
def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.find_by_email(current_user)
            if user.role != role:
                return jsonify(message=f'{role} access required'), 403
            else:
                return fn(*args, **kwargs)
        return wrapper
    return decorator


# Example route for registering a new user
@app.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    role = request.json.get('role', 'user')

    if not name or not email or not password or not role:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if a user with this email already exists
    if User.find_by_email(email):
        return jsonify({'message': 'Email address already registered'}), 400

    # Create the new user and save it to the database
    user = User(name, email, password, role)
    user.save()

    return jsonify({'message': 'User registered successfully'}), 201


# Example login endpoint that returns a JWT
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.find_by_email(email)
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # If the email and password are correct, generate and return a JWT token
    access_token = create_access_token(identity=user.email, expires_delta=timedelta(minutes=30))
    payload = {
        'access_token': access_token,
        'name': user.name,
        'email': user.email,
    }
    return jsonify(payload), 200


@app.route("/uni")
@jwt_required()
@role_required('user')
@cache.cached(timeout=30, query_string=True)
def get_universities():
    time.sleep(5)
    API_URL = "http://universities.hipolabs.com/search?country="
    search = request.args.get('c')
    if not search:
        search = "Pakistan"
    r = requests.get(f"{API_URL}{search}")
    return jsonify(r.json())


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        # port=5006
    )


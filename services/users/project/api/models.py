from sqlalchemy.sql import func

from project import db, bcrypt
from flask import current_app

import datetime
import jwt


# model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()
    
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username, 
            'email': self.email,
            'active': self.active
        }
    
    def encode_auth_token(self, user_id):
        """ Generates auth token """
        # given user_id encodes and returns a token
        try: 
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'), seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS') # expiration date
                ), 
                'iat': datetime.datetime.utcnow(), # issued at
                'sub': user_id # subject of token - user whom identifies
            }
            return jwt.encode(
                payload, 
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod       
    def decode_auth_token(auth_token):
        """ Decodes the auth_token - :param auth_token: - return: integer|string"""
        try: 
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY')
            )
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again'
        except jwt.InvalidError:
            return 'Invalid token. Please try again.'


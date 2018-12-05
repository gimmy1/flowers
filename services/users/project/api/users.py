from flask import Blueprint, jsonify, request
from project.api.models import User

from project import db # import SQLAlchemy

from sqlalchemy import exc

# create a new instance of Blueprint
flowers_blueprint = Blueprint('flowers', __name__)

# bound to flower()
@flowers_blueprint.route('/flowers/flower', methods=['GET'])
def flower():
    return jsonify({
        "flower": "soon"
    })

@flowers_blueprint.route('/flowers', methods=['GET'])
def get_all_users():
    """ Add flower user functionality && Retrieve all Users """
    response_object = {
        'message': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200

@flowers_blueprint.route('/flowers', methods=['POST', 'GET'])
def flower_user():
    post_data = request.get_json()
    response_object = {
        'message': 'Invalid payload'
    }

    # check for post_data
    if not post_data:
        return jsonify(response_object), 400
    
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email, password=password))
            db.session.commit()
            response_object['message'] = f'{email} was added'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That email already exists'
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify(response_object), 400
    

@flowers_blueprint.route('/flowers/<user_id>', methods=['GET'])
def get_single_user(user_id):
    response_object = {
        'message': 'User does not exist'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:    
            response_object = {
                'message': f'{user.email} exists',
                'data': {
                    'id': user.id,
                    'username': user.username, 
                    'email': user.email
                }
            }
            return jsonify(response_object), 200
    except ValueError as ve:
        return jsonify(response_object), 404
    




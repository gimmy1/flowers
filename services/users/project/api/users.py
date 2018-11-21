from flask import Blueprint, jsonify

# create a new instance of Blueprint
flowers_blueprint = Blueprint('flowers', __name__)

# bound to flower()
@flowers_blueprint.route('/flowers/flower', methods=['GET'])
def flower():
    return jsonify({
        "flower": "soon"
    })
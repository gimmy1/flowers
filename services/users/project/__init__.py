# services/users/project/__init__.py
from flask import Flask, jsonify
import os

app = Flask(__name__)
import pdb; pdb.set_trace()
# Pull in the config 
# Retrieve the environment variable with os.getenv // returns None if one does not exist
app_settings = os.getenv('APP_SETTINGS')
print(app_settings)
app.config.from_object('project.config.DevelopmentConfig')

@app.route('/flowers/flower', methods=['GET'])
def flower():
    return jsonify({
        "flower": "soon"
    })


# services/users/project/__init__.py
from flask import Flask, jsonify
import os

app = Flask(__name__)
# import pdb; pdb.set_trace()
# Pull in the config 
app.config.from_object('project.config.DevelopmentConfig')

@app.route('/flowers/flower', methods=['GET'])
def flower():
    return jsonify({
        "flower": "soon"
    })


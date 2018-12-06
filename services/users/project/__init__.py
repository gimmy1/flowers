# # services/users/project/__init__.py
# import os
# from flask import Flask, jsonify
# from flask_sqlalchemy import SQLAlchemy

# # instantiate the app
# app = Flask(__name__)

# # Pull in the config 
# # Retrieve the environment variable with os.getenv // returns None if one does not exist
# app_settings = os.getenv('APP_SETTINGS')
# app.config.from_object(app_settings)

# # instantiate the db
# db = SQLAlchemy(app)


import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# instantiate the db
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)
    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    # import pdb; pdb.set_trace()

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    

    # register blueprints
    from project.api.users import flowers_blueprint
    app.register_blueprint(flowers_blueprint)
    from project.api.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # shell context for cli
    # used to register app and db to the shell
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    
    return app
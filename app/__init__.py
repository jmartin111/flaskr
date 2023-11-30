#! .venv

import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.getenv("APP_SECRET_KEY"),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initial test route
    @app.route('/hello', methods=['GET'])
    def hello():
        return '<h1>HELLO</h1>'
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    return app
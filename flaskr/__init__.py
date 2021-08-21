import os
from flask import Flask
from flaskr.filters import timezone_filter

from . import db, auth, blog


def create_app(test_config=None):
    # create and configure the app
    flaskr_app = Flask(__name__, instance_relative_config=True)
    flaskr_app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(flaskr_app.instance_path, 'flaskr-tutorial.sqlite'),
        DEBUG=True,
        ENV='development'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        flaskr_app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        flaskr_app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(flaskr_app.instance_path)
    except OSError:
        pass

    db.init_app(flaskr_app)

    # various registries
    flaskr_app.register_blueprint(auth.bp)
    flaskr_app.register_blueprint(blog.bp)

    flaskr_app.add_url_rule('/', endpoint='index')

    flaskr_app.jinja_env.filters['timezone_filter'] = timezone_filter

    return flaskr_app


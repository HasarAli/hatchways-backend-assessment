from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.wsgi_app = DispatcherMiddleware(
        Response('Not Found', status=404),
        {'/api': app.wsgi_app}
    )

    @app.route('/ping')
    def ping():
        return {"success": True}

    return app

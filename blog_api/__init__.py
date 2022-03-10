from flask import Flask, jsonify
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

# Error handling from Flask Docs
class InvalidAPIUsage(Exception):
    def __init__(self, error, status_code=400, payload=None):
        super().__init__()
        self.error = error
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.error
        return rv


def handle_invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code


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

    from . import blog 
    app.register_blueprint(blog.bp)
    
    app.register_error_handler(InvalidAPIUsage, handle_invalid_api_usage)

    return app

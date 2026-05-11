from flask import Flask

def create_app():
    app = Flask(__name__)
    # Set a secret key for session management and flash messages
    app.secret_key = 'replace_this_with_a_random_secret_key'

    from . import routes
    app.register_blueprint(routes.bp)

    return app

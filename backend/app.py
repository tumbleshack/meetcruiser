import os

from flask import Flask, render_template_string
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore
from database import init_db, db_session
from models.user import User, Role
from passlib.totp import generate_secret
from apiflask import APIFlask  # step one
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_socketio import SocketIO, Namespace, emit

# Create app
app = APIFlask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
app.config.from_object('instance.config')

# Load the file specified by the APP_RUN_CONFIG environment variable
# Variables defined here will override those in the default configuration
env_config_module = os.environ.get('APP_RUN_CONFIG', 'config.development')
app.config.from_object(env_config_module)

# Enable CRSF protection on flask security too
# https://flask-security-too.readthedocs.io/en/stable/patterns.html#csrf
csrf = CSRFProtect(app)
socket_app = SocketIO(app, cors_allowed_origins=app.config['CORS_ORIGINS'], logger=True)

# Allow request from frontend domains
if (app.config['CORS_ORIGINS']):
    CORS(
        app,
        supports_credentials=True,  # needed for cross domain cookie support
        resources="/*",
        allow_headers="*",
        origins=app.config['CORS_ORIGINS'],
        expose_headers="Authorization,Content-Type,Authentication-Token,XSRF-TOKEN",
    )

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)

# Views
@app.route("/")
@auth_required()
def home():
    return render_template_string('Hello {{email}} !', email=current_user.email)

@app.route("/secret")
@auth_required()
def data():
    return "secret data"

class SecretNamespace(Namespace):
    def on_connect(self):
        print("connected!")
        pass

    def on_disconnect(self):
        print("disconnected!")
        pass

    def on_my_event(self, data):
        print("my_event", data)
        emit('my_response', {"data": "server response"})

socket_app.on_namespace(SecretNamespace('/test'))

# one time setup
with app.app_context():
    # Create a user to test with
    init_db()
    if not app.security.datastore.find_user(email="test@me.com"):
        app.security.datastore.create_user(email="test@me.com", password=hash_password("password"))
    db_session.commit()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    # run application (can also use flask run)
    socket_app.run(app)
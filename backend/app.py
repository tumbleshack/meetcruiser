import os

from flask import Flask, render_template_string
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore
from database import init_db, db_session
from models.user import User, Role
from passlib.totp import generate_secret
from apiflask import APIFlask  # step one
from flask_wtf.csrf import CSRFProtect

# Create app
app = APIFlask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
env_config_module = os.environ.get('APP_CONFIG_FILE', 'config.development')
app.config.from_object(env_config_module)

# Enable CRSF protection on flask security too
# https://flask-security-too.readthedocs.io/en/stable/patterns.html#csrf
csrf = CSRFProtect(app)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)

# Views
@app.route("/")
@auth_required()
def home():
    return render_template_string('Hello {{email}} !', email=current_user.email)

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
    app.run()
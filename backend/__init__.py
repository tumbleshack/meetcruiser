import os

from flask import Flask, render_template_string
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore
from sqlalchemy import select
from .decorators import auth_required_socket
from .models.swim import Event, Heat, Meet, Start, Strokes, Relay, Sex, Unit
from .database import init_db, db_session
from .models.user import User, Role
from passlib.totp import generate_secret
from apiflask import APIFlask  # step one
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_socketio import SocketIO, Namespace, emit
from .api import api_blueprint

class SecretNamespace(Namespace):
    @auth_required_socket()
    def on_connect(self):
        print("connected!")
    
    def on_disconnect(self):
        print("disconnected!")
        pass
    
    @auth_required_socket()
    def on_my_event(self, data):
        print("my_event", data)
        emit('my_response', {"data": "server response"})

# Create app
def create_app():
    app = APIFlask(__name__, instance_relative_config=True)

    # Load the default configuration
    app.config.from_object('backend.config.default')

    # Load the configuration from the instance folder
    app.config.from_object('backend.instance.config')

    # Load the file specified by the APP_RUN_CONFIG environment variable
    # Variables defined here will override those in the default configuration
    env_config_module = 'backend.config.' + os.environ.get('APP_RUN_CONFIG', 'development')
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

    socket_app.on_namespace(SecretNamespace('/test'))

# one time setup
    with app.app_context():
    # Create a user to test with
        init_db()
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(email="test@me.com", password=hash_password("password"))
        
            meet = Meet(name="Test Meet", current_start=0)
            db_session.add(meet)

            numStarts = 10
            for start_number in range(0, numStarts):
                start_query = Start(number=start_number, meet=meet)
                db_session.add(start_query)

            minAges = [0, 7, 9, 11, 13, 15] * 2
            maxAges = [6, 8, 10, 12, 14, 18] * 2
            sexes = [Sex.male, Sex.female] * 8
            strokes = [Strokes.freestyle, Strokes.backstroke, Strokes.breaststroke, Strokes.butterfly, Strokes.medley] * 3
            relays = [Relay.individual, Relay.individual, Relay.individual, Relay.relay] * 4
            distances = [25, 50, 100, 200, 400] * 3

            db_session.flush()
            # Create events and heats
            for event_number in range(1, 12):
                event = Event(
                    number=event_number, 
                    sex=sexes[event_number-1],
                    min_age=minAges[event_number-1],
                    max_age=maxAges[event_number-1],
                    stroke=strokes[event_number-1],
                    relay=relays[event_number-1],
                    distance=distances[event_number-1],
                    unit=Unit.yards,
                    meet=meet,
                )
                db_session.add(event)

                num_heats = 1
                for heat_number in range(1, num_heats+1):
                    start_num = min((event_number-1) * num_heats + (heat_number - 1), numStarts - 1)
                    start_query = select(Start).filter_by(number=start_num)
                    start = db_session.execute(start_query).scalar_one()
                    heat = Heat(number=heat_number, start=start, event=event)
                    db_session.add(heat)
        
            db_session.commit()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

# if __name__ == '__main__':
#     # run application (can also use flask run)
#     socket_app.run(app)

# app = create_app()
import os

from flask import Flask, render_template_string
from flask_cors import CORS
from flask_security import (
    Security,
    SQLAlchemySessionUserDatastore,
    auth_required,
    current_user,
    hash_password,
)
from flask_socketio import Namespace, SocketIO, emit
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import select

from .api import api_blueprint
from .app import app
from .database import db_session, init_db
from .decorators import auth_required_socket
from .models.swim import Event, Heat, Meet, Relay, Sex, Start, Strokes, Unit
from .models.user import Role, User


class SecretNamespace(Namespace):
    # @auth_required_socket()
    def on_connect(self):
        print("connected!")

    def on_disconnect(self):
        print("disconnected!")
        pass

    @auth_required_socket()
    def on_my_event(self, data):
        print("my_event", data)
        emit("my_response", {"data": "server response"})


# Create app
def create_app(enable_sockets=True):
    # Enable CRSF protection on flask security too
    # https://flask-security-too.readthedocs.io/en/stable/patterns.html#csrf
    csrf = CSRFProtect(app)

    # Allow request from frontend domains
    if ("CORS_ORIGINS" in app.config.keys()) and app.config["CORS_ORIGINS"]:
        CORS(
            app,
            supports_credentials=True,  # needed for cross domain cookie support
            resources="/*",
            allow_headers="*",
            origins=app.config["CORS_ORIGINS"],
            expose_headers="Authorization,Content-Type,Authentication-Token,XSRF-TOKEN",
        )

    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
    app.security = Security(app, user_datastore)

    if enable_sockets:
        socket_app = initialize_socket(app)
        socket_app.init_app(app)

    # one time setup
    with app.app_context():
        # Create a user to test with
        init_db()
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(
                email="test@me.com", password=hash_password("password")
            )

            meet = Meet(name="Test Meet", current_start=0)
            db_session.add(meet)

            numStarts = 10
            for start_number in range(0, numStarts):
                start_query = Start(number=start_number, meet=meet)
                db_session.add(start_query)

            minAges = [0, 7, 9, 11, 13, 15] * 2
            maxAges = [6, 8, 10, 12, 14, 18] * 2
            sexes = [Sex.male, Sex.female] * 8
            strokes = [
                Strokes.freestyle,
                Strokes.backstroke,
                Strokes.breaststroke,
                Strokes.butterfly,
                Strokes.medley,
            ] * 3
            relays = [
                Relay.individual,
                Relay.individual,
                Relay.individual,
                Relay.relay,
            ] * 4
            distances = [25, 50, 100, 200, 400] * 3

            db_session.flush()
            # Create events and heats
            for event_number in range(1, 12):
                event = Event(
                    number=event_number,
                    sex=sexes[event_number - 1],
                    min_age=minAges[event_number - 1],
                    max_age=maxAges[event_number - 1],
                    stroke=strokes[event_number - 1],
                    relay=relays[event_number - 1],
                    distance=distances[event_number - 1],
                    unit=Unit.yards,
                    meet=meet,
                )
                db_session.add(event)

                num_heats = 1
                for heat_number in range(1, num_heats + 1):
                    start_num = min(
                        (event_number - 1) * num_heats + (heat_number - 1),
                        numStarts - 1,
                    )
                    start_query = select(Start).filter_by(number=start_num)
                    start = db_session.execute(start_query).scalar_one()
                    heat = Heat(number=heat_number, start=start, event=event)
                    db_session.add(heat)

            db_session.commit()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app


def initialize_socket(app):
    if "CORS_ORIGINS" in app.config.keys():
        socket_app = SocketIO(
            app,
            cors_allowed_origins=app.config["CORS_ORIGINS"],
            logger=True,
            engineio_logger=True,
            log_output=True,
        )
    else:
        socket_app = SocketIO(app, logger=True, engineio_logger=True, log_output=True)
    socket_app.on_namespace(SecretNamespace("/test"))
    return socket_app

from apiflask import APIBlueprint
from flask import render_template_string
from flask_security import auth_required, current_user

test_blueprint = APIBlueprint('test', __name__)

@test_blueprint.route("/secret")
@auth_required()
def data():
    return "secret data"

# Views
@test_blueprint.route("/")
@auth_required()
def home():
    return render_template_string('Hello {{email}} !', email=current_user.email)
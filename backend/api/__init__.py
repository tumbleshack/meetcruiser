from apiflask import APIBlueprint

from .meet.routes import meet_blueprint
from .test.routes import test_blueprint

api_blueprint = APIBlueprint("api", __name__)
api_blueprint.register_blueprint(test_blueprint, url_prefix="/test")
api_blueprint.register_blueprint(meet_blueprint, url_prefix="/meet")

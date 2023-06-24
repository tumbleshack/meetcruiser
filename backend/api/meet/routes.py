from apiflask import APIBlueprint
from database import db_session
from models.swim import Meet
from sqlalchemy import select
from models import MeetSchema

meet_blueprint = APIBlueprint('meet', __name__)

@meet_blueprint.get("/<int:meet_id>")
@meet_blueprint.output(MeetSchema)
def get_meet(meet_id):
    meet_db = db_session.execute(select(Meet).filter_by(id=meet_id)).scalar_one()
    return MeetSchema().dump(meet_db)
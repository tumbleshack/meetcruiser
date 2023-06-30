from apiflask import APIBlueprint
from sqlalchemy import select

from backend.database import db_session
from backend.models import MeetSchema
from backend.models.swim import Meet

meet_blueprint = APIBlueprint("meet", __name__)


@meet_blueprint.get("/<int:meet_id>")
@meet_blueprint.output(MeetSchema)
def get_meet(meet_id):
    meet_db = db_session.execute(select(Meet).filter_by(id=meet_id)).scalar_one()
    return MeetSchema().dump(meet_db)

from sqlalchemy.orm import relationship, Mapped
from .swim import Team, UserTeamRole, Meet, team_meet_association, Event, Start, Heat
from .user import User, Role
from typing import Set, List

def configure_mappers():
    UserTeamRole.user = relationship(User)
    UserTeamRole.team = relationship(Team)
    UserTeamRole.role = relationship(Role)

    User.roles: Mapped[Set["Role"]] = relationship(UserTeamRole, back_populates="user", viewonly=True)
    Team.users: Mapped[Set["User"]] = relationship(UserTeamRole, back_populates="team", viewonly=True)
    User.teams: Mapped[Set["Team"]] = relationship(UserTeamRole, back_populates="user", viewonly=True)

    Meet.guest_teams: Mapped[List[Team]] = relationship(
        Team, secondary=team_meet_association, back_populates="guest_meets"
    )
    Team.guest_meets: Mapped[List[Meet]] = relationship(
        Meet, secondary=team_meet_association, back_populates="guest_teams"
    )
    Team.host_meets: Mapped[List[Meet]] = relationship(Meet, back_populates="host_team")

    Start.meet = relationship(Meet)
    Meet.starts: Mapped[List[Start]] = relationship(Start, back_populates="meet")
    Event.meet = relationship(Meet)
    Meet.events: Mapped[List[Event]] = relationship(Event, back_populates="meet")

    Heat.start = relationship(Start)
    Heat.event = relationship(Event)
    Start.heats: Mapped[List[Heat]] = relationship(Heat, back_populates="start")
    Event.heats: Mapped[List[Heat]] = relationship(Heat, back_populates="event")

configure_mappers()
from sqlalchemy.orm import relationship, Mapped
from .swim import Team, UserTeamRole
from .user import User, Role
from typing import Set

def configure_mappers():
    UserTeamRole.user = relationship(User)
    UserTeamRole.team = relationship(Team)
    UserTeamRole.role = relationship(Role)

    User.roles: Mapped[Set["UserTeamRole"]] = relationship(UserTeamRole, back_populates="user")

    Team.users: Mapped[Set["UserTeamRole"]] = relationship(UserTeamRole, back_populates="team")
    User.teams: Mapped[Set["UserTeamRole"]] = relationship(UserTeamRole, back_populates="user")

configure_mappers()
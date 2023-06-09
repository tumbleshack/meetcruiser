from .utils import TimestampMixin
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Column, Table
from typing import Optional

team_meet_association = Table(
    "team_meet_table",
    Base.metadata,
    Column("team_id", ForeignKey("team_table.id"), primary_key=True),
    Column("meet_id", ForeignKey("meet_table.id"), primary_key=True),
)

class Team(Base, TimestampMixin):
    __tablename__ = 'team_table'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), unique=True, nullable=False)
    description = mapped_column(String(255), nullable=True)
    
class UserTeamRole(Base, TimestampMixin):
    __tablename__ = 'user_team_role_table'
    id = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), unique=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team_table.id"), unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role_table.id"), unique=True)

class Meet(Base, TimestampMixin):
    __tablename__ = 'meet_table'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), unique=True, nullable=False)
    description = mapped_column(String(255), nullable=True)
    host_team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("team_table.id"))
    host_team: Mapped[Optional[Team]] = relationship(back_populates="host_meets")
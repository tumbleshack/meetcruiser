from .utils import TimestampMixin
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey

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
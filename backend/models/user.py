from .utils import TimestampMixin
from backend.database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import mapped_column
from sqlalchemy import Boolean, DateTime, Integer, String

class Role(Base, RoleMixin, TimestampMixin):
    __tablename__ = 'role_table'
    id = mapped_column(Integer(), primary_key=True)
    name = mapped_column(String(80), unique=True)
    description = mapped_column(String(255))

class User(Base, UserMixin, TimestampMixin):
    __tablename__ = 'user_table'
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(255), unique=True)
    username = mapped_column(String(255), unique=True, nullable=True)
    password = mapped_column(String(255), nullable=False)
    last_login_at = mapped_column(DateTime())
    current_login_at = mapped_column(DateTime())
    last_login_ip = mapped_column(String(100))
    current_login_ip = mapped_column(String(100))
    login_count = mapped_column(Integer)
    active = mapped_column(Boolean())
    fs_uniquifier = mapped_column(String(255), unique=True, nullable=False)
    confirmed_at = mapped_column(DateTime())
    tf_primary_method = mapped_column(String(64), nullable=True)
    tf_totp_secret = mapped_column(String(255), nullable=True)
    
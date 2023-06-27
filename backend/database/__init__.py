from sqlalchemy import create_engine, event, make_url
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import parse_qs, urlparse
from .rds_auth import get_new_connection
import importlib
import pathlib
import os

env_config_module = 'backend.config.' + os.environ.get('APP_RUN_CONFIG', 'development')
app_config = importlib.import_module('backend.config.default')
env_config = importlib.import_module(env_config_module)
app_config.__dict__.update(env_config.__dict__)

db_url = urlparse(app_config.SQLALCHEMY_DATABASE_URI)
path = pathlib.Path(db_url.path[1:])
path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)

# This is a hack to get SQLAlchemy to use the RDS IAM authentication token (lol autogenerated comment by Copilot)
if (app_config.SQLALCHEMY_DATABASE_URI.startswith('postgresql')):
    @event.listens_for(engine, "do_connect")
    def replace_connection(dialect, conn_rec, cargs, cparams):
        return get_new_connection(app_config.SQLALCHEMY_DATABASE_URI)
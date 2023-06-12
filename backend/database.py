from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import urlparse
import importlib
import pathlib
import os

env_config_module = os.environ.get('APP_RUN_CONFIG', 'config.development')
app_config = importlib.import_module('config.default')
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
    import models
    Base.metadata.create_all(bind=engine)
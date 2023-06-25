from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import urlparse
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


# def setup_schema(Base, session):
#     # Create a function which incorporates the Base and session information
#     def setup_schema_fn():
#         for class_ in Base.registry._class_registry.values():
#             if hasattr(class_, "__tablename__"):
#                 if class_.__name__.endswith("Schema"):
#                     raise ModelConversionError(
#                         "For safety, setup_schema can not be used when a"
#                         "Model class ends with 'Schema'"
#                     )

#                 class Meta(object):
#                     model = class_
#                     sqla_session = session

#                 schema_class_name = "%sSchema" % class_.__name__

#                 schema_class = type(
#                     schema_class_name, (SQLAlchemyAutoSchema,), {"Meta": Meta}
#                 )

#                 setattr(class_, "__marshmallow__", schema_class)

#     return setup_schema_fn

# event.listen(mapper, "after_configured", setup_schema(Base, db_session))

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)
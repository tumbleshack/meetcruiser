from apiflask import APIFlask
import os

def load_config(app):
    app.config.from_object('backend.config.default')
    app.config.from_object('backend.instance.default')

    # Load the file specified by the APP_RUN_CONFIG environment variable
    # Variables defined here will override those in the default configuration
    env_config_name = os.environ.get('APP_RUN_CONFIG', 'development')
    env_config_module = 'backend.config.' + env_config_name
    instance_config_module = 'backend.instance.' + env_config_name
    app.config.from_object(env_config_module)
    # Load the configuration from the instance folder
    app.config.from_object(instance_config_module)

app = APIFlask(__name__, instance_relative_config=True)
load_config(app)
## Backend 

### Building

Several pip packages need to be installed. Try installing them from requirements.txt. 

I have low confidence in the current requirements.txt, so if you notice anything missing, please feel free to make a PR updating it.

### Environment

**Instance Config**

The backend expects a few secrets to be be available in a directory `./backend/instance/`. Create two files in this directory:

1. `./backend/instance/__init__.py` (empty file) so python interprets the directory as a module
2. `./backend/instance/config.py` for the secrets

In `config.py`, the following secrets are mandatory:

```
SECRET_KEY = "Cryptographically-secure-seed"
SECURITY_PASSWORD_SALT = "Cryptographically-secure-salt-for-user-passwords"
SECURITY_TOTP_SECRETS = {1: "Cryptographically-secure-seed-for-MFA"}
```

**Run Config Module**

The backend reads configuration from the module specified by the `APP_RUN_CONFIG` environment variable. Set this variable to mirror a module in the `./backend/config` directory. I.E. one of

```
development
production
```


### Running

From the `./backend` directory, run
```
APP_RUN_CONFIG={development, production} python app.py
```

## Frontend

From the `./frontend` directory, use typical `npm` shortcuts for React. I.E. `npm run start` to run in development mode. See `./frontend/package.json` for details.


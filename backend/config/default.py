# Configuring Flask-Security-Too for single page web application (React)
# For more details, see:
# https://flask-security-too.readthedocs.io/en/stable/spa.html
# https://flask-security-too.readthedocs.io/en/stable/patterns.html#csrf
SECURITY_CSRF_COOKIE_NAME = 'XSRF-TOKEN'
WTF_CSRF_TIME_LIMIT = None
WTF_CSRF_CHECK_DEFAULT = False
SECURITY_CSRF_PROTECT_MECHANISMS = ['session']
SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
SECURITY_FLASH_MESSAGES = False
SECURITY_URL_PREFIX = '/api/auth'
SECURITY_REDIRECT_BEHAVIOR = 'spa'


# Enabling login features
SECURITY_REGISTERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TWO_FACTOR = True
SECURITY_TWO_FACTOR_ENABLED_METHODS = ['authenticator']
SECURITY_TOTP_ISSUER = 'TEST TOTP'
# SECURITY_OAUTH_ENABLE = True
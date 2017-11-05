# project/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    """Base configuration."""

    # main config
    SECRET_KEY = 'my_precious'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    DEBUG = False

    # mail settings
    # LOCAL FLASK
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # # SERVER MIME
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True

    # #OLD gmail authentication
    # MAIL_USERNAME = 'consensus.info@gmail.com'
    # MAIL_PASSWORD = 'consensusadmin2017'
    #NEW gmail authentification
    MAIL_USERNAME = 'noreply.consensus@gmail.com'
    MAIL_PASSWORD = 'consensus2017'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'consensus.info@gmail.com'

    # Consensus variables
    # Global variable support_rate_MIN = 80%
    SUPPORT_RATE_MIN = 80
    #
    SUPPORTERS_GOAL_NUM = 50
    #
    SUPPORTERS_CHAR_NUM_MAX = 35
    REJECTORS_CHAR_NUM_MAX = 80

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
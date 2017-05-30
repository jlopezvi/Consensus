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
    #MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    #MAIL_PORT = 587
    #MAIL_USE_TLS = True
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = 'consensus.info@gmail.com'
    MAIL_PASSWORD = 'consensusadmin'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'consensus.info@gmail.com'

    # Consensus variables
    # Global variable support_rate_MIN = 90%
    SUPPORT_RATE_MIN = 90

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
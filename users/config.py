from dotenv import load_dotenv

load_dotenv()
import os


def _get_bool_env_var(varname, default=None):
    value = os.getenv(varname, default)
    if value is None:
        return False
    elif isinstance(value, str) and value.lower() == 'false':
        return False
    elif bool(value) is False:
        return False
    else:
        return bool(value)


class BaseConfig(object):
    """Base configuration."""

    # main config
    SECRET_KEY = os.getenv('USER_SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('USER_SECURITY_PASSWORD_SALT')
    DEBUG = False

    # mail settings
    MAIL_SERVER = os.getenv('APP_MAIL_SERVER')
    MAIL_PORT = int(os.getenv('APP_MAIL_PORT'))
    MAIL_USE_TLS = _get_bool_env_var('APP_MAIL_USE_TLS')
    MAIL_USE_SSL = _get_bool_env_var('APP_MAIL_USE_SSL')

    # mail authentication
    MAIL_USERNAME = os.getenv('APP_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('APP_MAIL_PASSWORD')

    # mail accounts
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

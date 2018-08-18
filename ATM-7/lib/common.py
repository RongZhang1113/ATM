from core import src
from conf import settings
import logging.config


def login_auth(func):
    def auth(*args, **kwargs):
        if not src.user_data['name']:
            src.login()
        return func(*args, **kwargs)

    return auth


def get_logger(name):
    logging.config.dictConfig(settings.LOGGING_DIC)
    me_log = logging.getLogger(name)
    return me_log

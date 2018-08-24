from core import src
from conf import settings
import logging.config


def login_auth(func):
    '''
    # 用户登录认证装饰器
    :param func:
    :return:
    '''
    def auth(*args, **kwargs):
        if not src.user_data['name']:
            src.login()
            # 登录后直接跳转至用户选择的功能
            if src.user_data['name']:
                return func(*args, **kwargs)
            # 用于结束函数（用户输入三次之后）
            return
        return func(*args, **kwargs)

    return auth


def get_logger(name):
    '''
    # 获取日志
    :param name: 日志名
    :return:
    '''
    logging.config.dictConfig(settings.LOGGING_DIC)
    me_log = logging.getLogger(name)
    return me_log

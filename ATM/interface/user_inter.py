from db import handler
from lib.common import get_logger

user_log = get_logger('user')


def register_interface(name, password):
    user_dic = handler.select(name)
    if user_dic:
        return False, '用户已存在'
    else:
        dic = {'name': name,
               'pwd': password,
               'balance': 20000,
               'locked': False,
               'bank_flow': [],
               'shopping_cart': {}}
        handler.save(dic)
        user_log.info('%s 注册成功' % name)
        return True, '%s 注册成功' % name


def login_interface(name, password):
    user_dic = handler.select(name)
    if user_dic:
        if password == user_dic['pwd']:
            return True, '%s 登录成功' % name
        else:
            return False, '密码错误'
    return False, '该用户不存在'


def locked_interface(name):
    user_dic = handler.select(name)
    if user_dic:
        user_dic['locked'] = True
        handler.save(user_dic)



def unlock_interface(name):
    user_dic = handler.select(name)
    if user_dic:
        user_dic['locked'] = False
        handler.save(user_dic)

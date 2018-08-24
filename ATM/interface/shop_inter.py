from db import handler
from lib.common import get_logger
from interface import bank_inter

user_log = get_logger('user')


def shopping_interface(name, cost, shopping_cart):
    flg, msg = bank_inter.cost_interface(name, cost)
    if flg:
        user_dic = handler.select(name)
        user_dic['shopping_cart'] = shopping_cart
        handler.save(user_dic)
        return True, '购买成功，静待发货'
    return False, 'nothing'


def check_shopping_cart_interface(name):
    dic = handler.select(name)
    return dic['shopping_cart']

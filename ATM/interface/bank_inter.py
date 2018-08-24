from db import handler
from lib.common import get_logger

user_log = get_logger('bank')


def transfer_interface(to_name, from_name, balance):
    to_dic = handler.select(to_name)
    if to_dic:
        from_dic = handler.select(from_name)
        if from_dic['balance'] >= balance:
            to_dic['balance'] += balance
            from_dic['balance'] -= balance
            to_dic['bank_flow'].append('%s 向您转账 %s 元' % (from_name, balance))
            from_dic['bank_flow'].append('您向 %s 转账 %s 元' % (to_name, balance))
            user_log.info('%s 给 %s 转账 %s 元' % (from_name, to_name, balance))
            handler.save(to_dic)
            handler.save(from_dic)
            return True, '转账成功 %s 元' % balance
        return False, '余额不足'
    return False, '对方账户不存在'


def repay_interface(name, balance):
    dic = handler.select(name)
    if dic:
        dic['balance'] += balance
        dic['bank_flow'].append('还款 %s 元' % balance)
        handler.save(dic)
        user_log.info('还款 %s 元' % balance)
        return True, '还款成功 %s 元' % balance
    return False, 'fail'


def withdraw_interface(name, balance):
    dic = handler.select(name)
    money = balance * 1.05
    if dic['balance'] >= money:
        dic['balance'] -= money
        dic['bank_flow'].append('取款 %s 元' % balance)
        user_log.info('取款 %s 元' % balance)
        handler.save(dic)
        return True, '取款成功 %s 元' % balance
    return False, '余额不足'


def check_balance_interface(name):
    dic = handler.select(name)
    return dic['balance']


def check_flow_interface(name):
    dic = handler.select(name)
    user_log.info('%s 查看了流水' % name)
    return dic['bank_flow']


def cost_interface(name, cost):
    dic = handler.select(name)
    if dic['balance'] >= cost:
        dic['balance'] -= cost
        dic['bank_flow'].append('购物消费 %s 元' % cost)
        user_log.info('购物消费 %s 元' % cost)
        return True, 'success'
    return False, 'fail'

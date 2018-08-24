import time
from interface import user_inter, bank_inter, shop_inter
from lib.common import login_auth


user_data = {'name': None}


def register():
    print('注册')
    if user_data['name']:
        print('您已登录，无需注册')
        return
    while True:
        name = input('请输入用户名或按(q/Q)退出>>:').strip()
        if name == 'q' or name == 'Q': break
        if len(name) == 0:continue
        pwd = input('请输入密码>>:').strip()
        if len(pwd) == 0: continue
        conf_pwd = input('请再次输入密码>>:').strip()
        if pwd == conf_pwd:
            flag, msg = user_inter.register_interface(name, pwd)
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print('两次密码输入不一致，请重试')


def login():
    print('登录')
    if user_data['name']:
        print('您已登录')
        return
    count = 0
    while True:
        name = input('请输入用户名>>:').strip()
        if len(name) == 0: continue
        pwd = input('请输入密码>>:').strip()
        if len(pwd) == 0: continue
        flag, msg = user_inter.login_interface(name, pwd)
        if flag:
            print(msg)
            # 登录后记录用户名，以备下次使用
            user_data['name'] = name
            break
        else:
            print(msg)
            count += 1
            if count > 2:
                # 以下功能不完善
                user_inter.locked_interface(name)
                print('尝试次数过多，已退出')
                break


@login_auth
def withdraw():
    print('取款')
    num = []
    for i in range(51):
        num.append(i)
    balance = input('请输入取款金额或按(q/Q)退出>>:').strip()
    if balance == 'q' or balance == 'Q': return
    if balance.isdigit():
        balance = int(balance)
        if balance / 100 in num:
            flag, msg = bank_inter.withdraw_interface(user_data['name'], balance)
            if flag:
                print(msg)
            else:
                print(msg)
        else:
            print('单笔提现不能超过5000，且不支持取零')
    else:
        print('必须输入整数')


@login_auth
def repay():
    print('还款')
    num = []
    for i in range(101):
        num.append(i)
    balance = input('请输入取款金额或按(q/Q)退出>>:').strip()
    if balance == 'q' or balance == 'Q': return
    if balance.isdigit():
        balance = int(balance)
        if balance / 100 in num:
            flag, msg = bank_inter.repay_interface(user_data['name'], balance)
            if flag:
                print(msg)
            else:
                print(msg)
        else:
            print('单笔还款不能超过10000，且不支持存零')
    else:
        print('必须输入整数')


@login_auth
def transfer():
    print('转账')
    to_name = input('请输入对方账户名或按(q/Q)退出>>:').strip()
    if to_name == 'q' or to_name == 'Q': return
    balance = input('请输入取款金额或按(q/Q)退出>>:').strip()
    if balance == 'q' or balance == 'Q': return
    if balance.isdigit():
        balance = int(balance)
        flag, msg = bank_inter.transfer_interface(user_data['name'], to_name, balance)
        if flag:
            print(msg)
        else:
            print(msg)
    else:
        print('必须输入整数')


@login_auth
def check_balance():
    flag = bank_inter.check_balance_interface(user_data['name'])
    print('您的余额为：%s 元' % flag)


@login_auth
def check_flow():
    flag = bank_inter.check_flow_interface(user_data['name'])
    for info in flag:
        print('您的交易信息：%s' % info)


@login_auth
def check_shop_cart():
    flag = shop_inter.check_shopping_cart_interface(user_data['name'])
    print(flag)


@login_auth
def shopping():
    print('购物')
    goods_list = [
        ['武直十', 100000000],
        ['風雲4號衛星', 900000000],
        ['一節車皮', 80000],
        ['腎', 250000],
        ['坦克', 100000],
        ['飛機頭', 30000000]
    ]
    cost = 0
    shopping_cart = {}
    curr_balance = bank_inter.check_balance_interface(user_data['name'])
    while True:
        for k, v in enumerate(goods_list):
            print('%s %s' % (k, v))
        choice = input('选择购买的商品编号或按(q/Q)退出>>:').strip()
        if choice.isdigit():
            choice = int(choice)
            if choice >= 0 and choice <= 4:
                goods_name = goods_list[choice][0]
                goods_price = goods_list[choice][1]
                if goods_price <= curr_balance:
                    if goods_name in shopping_cart:
                        shopping_cart[goods_name]['count'] += 1
                    else:
                        shopping_cart[goods_name] = {'price': goods_price, 'count': 1}
                    curr_balance -= goods_price
                    cost += goods_price
                else:
                    print('余额不足，兄带')
            else:
                print('没有该商品')
            print('购物详单 %s' % shopping_cart)
        elif choice == 'q' or choice == 'Q':
            print('您的购物详单:%s'%shopping_cart)
            print('您已花费 %s 元' % cost)
            if cost == 0:break
            buy = input('确认购买？(y/n)>>:').strip()
            if buy == 'y' or buy == 'Y':
                flg, msg = shop_inter.shopping_interface(user_data['name'], cost, shopping_cart)
                if flg:
                    print(msg)
                    break
                else:
                    print(msg)
                    break
            else:
                print('nothing')

        else:
            print('wrong')


func_dic = {
    '1': register,
    '2': login,
    '3': transfer,
    '4': withdraw,
    '5': repay,
    '6': shopping,
    '7': check_balance,
    '8': check_flow,
    '9': check_shop_cart
}


def run():
    while True:
        time.sleep(0.1)   # 模拟系统的网络延时
        print('''
        1 注册
        2 登录
        3 转账
        4 取款
        5 还款
        6 购物
        7 查看余额
        8 查看流水
        9 购物车记录
        0 退出        
        ''')
        choice = input('please choose>>:').strip()
        if choice == '0':
            # 申明全局变量，用户退出后将用户信息清空
            global user_data
            user_data['name'] = None
            break
        if choice not in func_dic:
            print('没有该选项，请重试')
            continue
        func_dic[choice]()

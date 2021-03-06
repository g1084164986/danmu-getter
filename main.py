import time, sys
import re

from termcolor import *
from danmu import DanMuClient

douyu = {'825': '嘉年华火箭', '195': '飞机', '750': '办卡', '193': '弱鸡', '192': '赞',
         '826': '嘉年华蛋糕', '824': '粉丝荧光棒', '712': '棒棒哒', '714': '怂', '713': '辣眼睛',
         '520': '稳',
         'cq': '酬勤'}


# Generate content
def gift_content(msg):
    if re.match(r'^(?:http://)?.*?live.bilibili.com/(.+?)$', sys.argv[1]):
        msg['Content'] = msg['data']['giftName']
    elif re.match(r'^(?:http://)?.*?douyu.com/(.+?)$', sys.argv[1]):
        msg['Content'] = msg['gfid']
        if msg['Content'] in douyu:
            msg['Content'] = douyu[msg['Content']]
    else:
        pass


# print format
def pd(msg):
    if 'nodanmu' not in sys.argv:
        print(msg)


def pg(msg):
    if 'nogift' not in sys.argv:
        print(colored(msg, 'yellow'))


if sys.argv.__len__() is 1:
    print('usage: main.py [url] <parameter>')
    exit()


# create client
dmc = DanMuClient(sys.argv[1].strip())

if not dmc.isValid():
    print('Url not valid')
    exit()


# print action
@dmc.danmu
def danmu_fn(msg):
    pd('[%s] %s' % (msg['NickName'], msg['Content']))
    # pass


@dmc.gift
def gift_fn(msg):
    gift_content(msg)
    pg('[%s] 赠送了%s' % (msg['NickName'], msg['Content']))


@dmc.other
def other_fn(msg):
    pass


print('Connecting...')
dmc.start(blockThread=True)

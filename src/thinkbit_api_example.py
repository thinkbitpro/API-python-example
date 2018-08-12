# coding=utf-8
'''
Created on Mar 11, 2018

@author: gjwang
'''

import time

from thinkbit import ThinkBitClient

API_KEY = 'cae9b026ec117935a0530a2fbc70445c'
API_SECRET = '5d6bd9b6d74da2eb869bbc2d58a79d0468139dd49674c547bb06b2074d6b0e27'

if __name__ == '__main__':
    tbClient = ThinkBitClient(API_KEY, API_SECRET)

    # 查询各币种
    tbClient.check_balance(currency='BTC')
    time.sleep(0.1)
    tbClient.check_balance(currency='ETH')
    time.sleep(0.1)
    tbClient.check_balance(currency='BCH')

    # 限价卖出
    time.sleep(0.1)
    tbClient.sell_limit(pair='BCH_BTC', price=0.1, amount=0.3)

    # 限价买入
    time.sleep(0.1)
    tbClient.buy_limit(pair='BCH_BTC', price=0.1, amount=0.1)

    # 市价买入
    time.sleep(0.1)
    tbClient.buy_market(pair='BCH_BTC', amount=0.1)

    # 市价卖出
    time.sleep(0.1)
    tbClient.sell_market(pair='BCH_BTC', amount=0.1)

    # 准备订单以备撤销
    time.sleep(0.1)
    order_id = tbClient.buy_limit(pair='BCH_BTC', price=0.2, amount=0.1)

    # 撤销订单
    time.sleep(0.1)
    tbClient.cancel_order(order_id=order_id)

    # 查询所有未成交限价单
    time.sleep(1)
    tbClient.query_order()

    # 查询所有生效订单
    time.sleep(1)
    tbClient.query_active_order('EOS_USDT')

    # 查询已成交市价单
    time.sleep(1)
    tbClient.query_closed_order()

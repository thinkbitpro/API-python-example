# -*- coding: utf-8 -*-

'''
Created on Mar 10, 2018

@author: gjwang
'''

import hmac
import json
import os.path
import time
from hashlib import sha512

import requests

API_BASE_URL = 'https://api.thinkbit.com/v1/'

API_PATH = {
    'checkBalance': 'account/balance',
    'createOrder': 'order/create',
    'queryOrder': 'order/query',
    'queryClosedOrder': 'order/query/closed',
    'queryActiveOrder': 'order/active',
    'cancel': 'order/cancel',
}


class ThinkBitClient(object):
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret

    # 签名函数
    def sign(self, data):
        sign = hmac.new(self.api_secret, data, sha512)
        headers = {'api_key': self.api_key,
                   'signature': sign.hexdigest()
                   }
        return headers

    def get(self, path, params=None):
        pass

    def post(self, url, data=None):
        if data is not None:
            nonce = int(time.time() * 1000)
            data['nonce'] = nonce

        data_str = json.dumps(data, separators=(',', ':'))
        headers = self.sign(data_str)

        # TODO limit send request frequent
        ret = requests.post(url, data=data_str, headers=headers)
        print('ret.text', ret.text)

        ret_dict = {}
        if ret.text:
            ret_dict = json.loads(ret.text)
        return ret_dict

    # 查询余额
    # currency 币种
    def check_balance(self, currency=None):
        url = os.path.join(API_BASE_URL, API_PATH['checkBalance'])
        data = {'currency': currency}
        self.post(url, data)

    # 买入限价单
    # pair 交易对名称
    # price 报价
    # amount 报量
    def buy_limit(self, pair, price, amount):
        url = os.path.join(API_BASE_URL, API_PATH['createOrder'])
        data = {"pair": pair,
                "side": "buy",
                "type": "limit",
                "price": price,
                "amount": amount
                }
        order_id = self.post(url, data)["order_id"]
        print('buy order_id=', order_id)
        return order_id

    # 买入市价单
    # pair 交易对名称，字符串
    # amount 报量，数字
    def buy_market(self, pair, amount):
        url = os.path.join(API_BASE_URL, API_PATH['createOrder'])
        data = {"pair": pair,
                "side": "buy",
                "type": "market",
                "amount": amount
                }
        order_id = self.post(url, data)["order_id"]
        print('buy order_id=', order_id)
        return order_id

    # 卖出限价单
    # pair 交易对名称
    # price 报价
    # amount 报量
    def sell_limit(self, pair, price, amount):
        url = os.path.join(API_BASE_URL, API_PATH['createOrder'])
        data = {"pair": pair,
                "side": "sell",
                "type": "limit",
                "price": price,
                "amount": amount
                }
        order_id = self.post(url, data)["order_id"]
        print('sell order_id=', order_id)
        return order_id

    # 卖出市价单
    # pair 交易对名称，字符串
    # amount 报量，数字
    def sell_market(self, pair, amount):
        url = os.path.join(API_BASE_URL, API_PATH['createOrder'])
        data = {"pair": pair,
                "side": "sell",
                "type": "market",
                "amount": amount
                }
        order_id = self.post(url, data)["order_id"]
        print('sell order_id=', order_id)
        return order_id

    # 查询未成交的限价单
    # order_id 订单号，不填则返回所有未成交订单
    def query_order(self, order_id=None):
        url = os.path.join(API_BASE_URL, API_PATH['queryOrder'])
        data = {"order_id": order_id}
        self.post(url, data)

    # 查询已成交的市价单
    # order_id 订单号，不填则返回所有已成交订单
    def query_closed_order(self, order_id=None):
        url = os.path.join(API_BASE_URL, API_PATH['queryClosedOrder'])
        data = {"order_id": order_id}
        self.post(url, data)

    # 查询当前生生效订单
    # pair 交易对名称
    def query_active_order(self, pair):
        url = os.path.join(API_BASE_URL, API_PATH['queryActiveOrder'])
        data = {'pair': pair}
        self.post(url, data)

    # 撤销订单
    # order_id 订单号
    def cancel_order(self, order_id=None):
        if not order_id:
            return
        url = os.path.join(API_BASE_URL, API_PATH['cancel'])
        data = {"order_id": order_id}
        self.post(url, data)

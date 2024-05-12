import asyncio
import logging
import math
import os
import pprint
import threading
import time
from datetime import datetime
from enum import Enum

import pandas as pd
import pytz
from binance.exceptions import BinanceAPIException

from binance_stream_manager import *

# GLOBAL CONSTANTS
MAKS_MARGIN = 1.0
MIN_MARGIN = 0.0

stream = BinanceStreamManager()
stream.start()


class Side(Enum):
    LONG = 1
    SHORT = 2


class Position:
    def __init__(self):
        self.id = 0
        self.bep = 0.0
        self.symbol = ""
        self.side = None
        self.pos_amt = 0.0
        self.margin = 0.0
        self.entry_price = 0.0
        self.roi = 0.0
        self.pnl = 0.0
        self.leverage = 0
        # self.init()

    def init(self, pos_info):
        # pos_info = pd.DataFrame(stream.client.futures_position_information(symbol=stream.SYMBOL))
        self.entry_price = float(pos_info['entryPrice'])
        self.bep = float(pos_info['breakEvenPrice'])
        self.leverage = int(pos_info['leverage'])
        self.symbol = pos_info['symbol']
        self.pos_amt = float(pos_info['positionAmt'])
        self.margin = abs(self.pos_amt) * self.entry_price / self.leverage
        if self.pos_amt == 0.0:
            self.side = None

        else:
            if self.pos_amt > 0:
                self.side = Side.LONG

            if self.pos_amt < 0:
                self.side = Side.SHORT

    def update(self):
        self.bep = stream.account_update[2]
        self.entry_price = stream.account_update[3]
        self.pos_amt = stream.account_update[4]
        self.symbol = stream.account_update[5]
        self.margin = abs(self.pos_amt) * self.entry_price / self.leverage
        if self.pos_amt == 0.0:
            self.side = None

        else:
            if self.pos_amt > 0:
                self.side = Side.LONG

            if self.pos_amt < 0:
                self.side = Side.SHORT

    def close_short_position(self, ratio):
        stream.client.futures_create_order(
            symbol=self.symbol,
            side='BUY',
            type='MARKET',
            quantity=math.ceil((float(abs(self.pos_amt)) * ratio) * 10) / 10,
            reduceOnly='True'
        )

    def close_long_position(self, ratio):
        stream.client.futures_create_order(
            symbol=self.symbol,
            side='SELL',
            type='MARKET',
            quantity=math.ceil((float(abs(self.pos_amt)) * ratio) * 10) / 10,
            reduceOnly='True'
        )


class Account:
    def __init__(self):
        self.balance = float(stream.client.futures_account()['totalWalletBalance'])
        self.balance_change = 0.0
        self.positions: dict = {}
        self.threshold = -10
        self.done = [False, False, False, False]

        while not self.positions:
            stream.account_update = []
            for item in stream.client.futures_position_information():
                if item['entryPrice'] != '0.0':
                    stream.run_socket(item['symbol'])
                    while stream.streams[item['symbol']]['currentCandle'].close == 0.0:
                        time.sleep(0.5)
                    position = Position()
                    position.init(item)
                    self.positions[item['symbol']] = position
                    t = threading.Thread(target=self._position_listener, args=(handle_position_listener, position,))
                    t.start()

            if not self.positions:
                while not stream.account_update:
                    time.sleep(1)

    def _position_listener(self, callback, p):
        while True:
            if stream.account_update:
                self.balance_change = stream.account_update[0]
                self.balance = stream.account_update[1]
                self.positions[stream.account_update[5]].update()
                stream.account_update = []
            while p.side:
                p.pnl = (stream.streams[p.symbol]['currentCandle'].close - p.bep) * p.pos_amt
                p.roi = (p.pnl / p.margin) * 100

                if self.threshold > p.roi:
                    if p.side == Side.SHORT:
                        p.close_short_position(1)
                    elif p.side == Side.LONG:
                        p.close_long_position(1)
                    self.threshold = -10
                    self.done = [False, False, False, False]
                elif p.roi > 3 and not self.done[0]:
                    self.threshold = 1
                    self.done[0] = True
                elif p.roi > 15 and not self.done[1]:
                    if p.side == Side.SHORT:
                        p.close_short_position(0.5)
                    elif p.side == Side.LONG:
                        p.close_long_position(0.5)
                    self.done[1] = True
                elif p.roi > 30 and not self.done[2]:
                    if p.side == Side.SHORT:
                        p.close_short_position(0.5)
                    elif p.side == Side.LONG:
                        p.close_long_position(0.5)
                    self.done[2] = True
                    self.threshold = 15
                elif p.roi >= 50 and not self.done[3]:
                    if p.side == Side.SHORT:
                        p.close_short_position(0.5)
                    elif p.side == Side.LONG:
                        p.close_long_position(1)
                    self.done[3] = True

                if stream.account_update:
                    self.balance_change = stream.account_update[0]
                    self.balance = stream.account_update[1]
                    p.update()
                callback([p.pnl, p.roi, self.balance, p.symbol])
                time.sleep(0.5)
            time.sleep(0.5)

    # CLIENT FUNCTIONS

    # def set_quantity(self, ratio):
    #     quantity = 0.0
    #     res_margin = 0.0
    #     if ratio == 0.0:
    #         res_margin = 5.0
    #         min_q = res_margin / stream.current_candle.close
    #         return math.ceil(min_q * 10) / 10
    #     while res_margin < ratio * (self.balance * self.leverage - (self.balance * self.leverage) * 0.001):
    #         quantity += 0.1
    #         res_margin = quantity * stream.current_candle.close
    #     return quantity

    # def create_short_position(self):
    #     stream.client.futures_change_leverage(symbol=self.symbol, leverage=self.leverage)
    #     try:
    #         stream.client.futures_create_order(
    #             symbol=stream.SYMBOL,
    #             type='MARKET',
    #             side='SELL',
    #             quantity=self.set_quantity(MIN_MARGIN)
    #         )
    #         tz_turkey = pytz.timezone('Europe/Istanbul')
    #         datetime_turkey = datetime.now(tz_turkey)
    #         current_time = datetime_turkey.strftime("%H:%M:%S")
    #         print(f"\rSHORT: {stream.current_candle.close}", current_time)
    #         logging.info(current_time)
    #         self.side = Side.SHORT
    #     except BinanceAPIException as err:
    #         if err.code == -2019:
    #             print(err.message)
    #             logging.error(err.message)
    #             raise BinanceAPIException(err.response, err.status_code, err.message)
    #         else:
    #             logging.exception('Create short exception occured:')
    #             raise BinanceAPIException(err.response, err.status_code, err.message)

    # def create_long_position(self):
    #     stream.client.futures_change_leverage(symbol=self.symbol, leverage=self.leverage)
    #     try:
    #         stream.client.futures_create_order(
    #             symbol=stream.SYMBOL,
    #             type='MARKET',
    #             side='BUY',
    #             quantity=self.set_quantity(MIN_MARGIN)
    #         )
    #         tz_turkey = pytz.timezone('Europe/Istanbul')
    #         datetime_turkey = datetime.now(tz_turkey)
    #         current_time = datetime_turkey.strftime("%H:%M:%S")
    #         print(f"\rLONG: {stream.current_candle.close}", current_time)
    #         logging.info(current_time)
    #         self.side = Side.SHORT
    #     except BinanceAPIException as err:
    #         if err.code == -2019:
    #             print(err.message)
    #             logging.error(err.message)
    #             raise BinanceAPIException(err.response, err.status_code, err.message)
    #         else:
    #             logging.exception('Create long exception occured:')
    #             raise BinanceAPIException(err.response, err.status_code, err.message)


def handle_position_listener(msg):
    print(f"\r{msg[3]}>> Pnl: {msg[0]:.2f}, Roi: {msg[1]:.2f}, Balance: {msg[2]:.2f}", end="", flush=True)

# def test():
#     acc = Account()
#
#
# if __name__ == "__main__":
#     test()

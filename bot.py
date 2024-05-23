import asyncio
import logging
import math
import os
import pprint
import threading
import time
from datetime import datetime
from enum import Enum, auto
import binance
from reprint import output
import pandas as pd
import talib as ta
import pytz
from binance.exceptions import BinanceAPIException

from binance_stream_manager import *
from utils.helpers import *

# GLOBAL CONSTANTS
MAKS_MARGIN = 1.0
MIN_MARGIN = 0.0

_i = 0
stream = BinanceStreamManager()
stream.start()


class Side(Enum):
    LONG = 1
    SHORT = 2


class Position:
    def __init__(self):
        self.total_pos_amt = 0.0
        self.id = 0
        self.bep = 0.0
        self.symbol = ""
        self.side = None
        self.pos_amt = 0.0
        self.margin = 0.0
        self.entry_price = 0.0
        self.roi = 0.0
        self.pnl = 0.0
        self.total_pnl = 0.0
        self.leverage = 0
        self.fe = 0.0  # fast ema
        self.se = 0.0  # slow ema
        self.vse = 0.0  # very slow ema
        # self.init()

    def init(self, pos_info):
        # pos_info = pd.DataFrame(stream.client.futures_position_information(symbol=stream.SYMBOL))
        self.entry_price = float(pos_info['entryPrice'])
        self.bep = float(pos_info['breakEvenPrice'])
        self.leverage = int(pos_info['leverage'])
        self.symbol = pos_info['symbol']
        self.pos_amt = float(pos_info['positionAmt'])
        self.margin = abs(self.pos_amt) * self.entry_price / self.leverage
        self.fe = stream.streams[self.symbol]['fast_ema'][-1]
        self.se = stream.streams[self.symbol]['slow_ema'][-1]
        self.vse = stream.streams[self.symbol]['very_slow_ema'][-1]
        if self.pos_amt == 0.0:
            self.side = None

        else:
            if self.pos_amt > 0:
                self.side = Side.LONG

            if self.pos_amt < 0:
                self.side = Side.SHORT

    def update(self):
        self.bep = stream.account_update[2] if not None else 0.0
        self.entry_price = stream.account_update[3] if not None else 0.0
        self.pos_amt = stream.account_update[4] if not None else 0.0
        self.margin = abs(self.pos_amt) * self.entry_price / self.leverage if not None else 0.0

        if self.pos_amt == 0.0 or self.entry_price is None:
            self.total_pos_amt = stream.account_update[4] if not None else 0.0
        self.symbol = stream.account_update[5] if not None else ""
        if self.pos_amt == 0.0 or None:
            self.side = None

        else:
            if self.pos_amt > 0:
                self.side = Side.LONG

            if self.pos_amt < 0:
                self.side = Side.SHORT

    def close_short_position(self, ratio):
        global _i
        try:
            stream.client.futures_create_order(
                symbol=self.symbol,
                side='BUY',
                type='MARKET',
                quantity=self.get_quantity(ratio),
                reduceOnly='True'
            )
        except binance.exceptions.BinanceAPIException as err:
            if err.code == -2022:
                if _i == 4:
                    raise binance.exceptions.BinanceAPIException(err.response, err.status_code, err.message)
                else:
                    time.sleep(1)
                    _i += 1
                    self.close_short_position(ratio)
                    _i = 0

    def close_long_position(self, ratio):
        global _i
        try:
            stream.client.futures_create_order(
                symbol=self.symbol,
                side='SELL',
                type='MARKET',
                quantity=self.get_quantity(ratio),
                reduceOnly='True'
            )
        except binance.exceptions.BinanceAPIException as err:
            if err.code == -2022:
                if _i == 4:
                    raise binance.exceptions.BinanceAPIException(err.response, err.status_code, err.message)
                else:
                    time.sleep(1)
                    _i += 1
                    self.close_long_position(ratio)
                    _i = 0

    def get_quantity(self, ratio):
        amount = abs(self.pos_amt) / self.min_qty()  # dividable integer amount
        # assert amount.is_integer()
        amount = int(amount * ratio)
        if amount == 0:
            return self.min_qty()
        else:
            min_q = str(self.min_qty())
            if min_q.isdigit():
                min_q = int(min_q)
                return str(int(amount * min_q))
            else:
                min_q = float(min_q)
                return str(float(amount * min_q))

    def set_amt(self, num):
        self.pos_amt = num

    def min_qty(self):
        list_ = stream.client.futures_exchange_info()['symbols']
        for info in list_:
            if info.get('symbol') == self.symbol:
                for filter_ in info['filters']:
                    if filter_['filterType'] == 'LOT_SIZE':
                        min_qty = filter_['minQty']
                        if min_qty.isdigit():
                            min_qty = int(min_qty)
                        else:
                            min_qty = float(min_qty)
                        return min_qty


class Account:
    def __init__(self, is_test=False):
        self.is_test = is_test
        self.balance = float(stream.client.futures_account()['totalWalletBalance'])
        self.balance_change = 0.0
        self.positions: dict = {}
        self.threshold = -4
        self.done = [False, False, False, False]
        self.check_list = ["", "", "", ""]
        if self.is_test:
            print("Test mode")

        while not self.positions:
            stream.account_update = []
            if not is_test:
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
            else:
                self.set_test_position('PENDLEUSDT')

            if not self.positions:
                while not stream.account_update:
                    time.sleep(1)

    def _position_listener(self, callback, p):
        while True:
            if stream.account_update:
                self.balance_change = stream.account_update[0]
                self.balance = stream.account_update[1]
                self.positions[stream.account_update[5]].update()
                p.update()
                stream.account_update = []
            while p.side:
                p.pnl = (stream.streams[p.symbol]['currentCandle'].close - p.entry_price) * p.pos_amt
                p.roi = (p.pnl / p.margin) * 100

                if self.threshold > p.roi:
                    if p.side == Side.SHORT:
                        p.close_short_position(1) if not self.is_test else print(p.get_quantity(1)), p.update
                    elif p.side == Side.LONG:
                        p.close_long_position(1) if not self.is_test else print(p.get_quantity(1)), p.update

                    if p.side == Side.SHORT:
                        if self.threshold < 0:
                            self.create_long_position(p.symbol) if not self.is_test else print(p.get_quantity(1)), p.update
                        else:
                            self.create_short_position(p.symbol) if not self.is_test else print(p.get_quantity(1)), p.update
                    elif p.side == Side.LONG:
                        if self.threshold < 0:
                            self.create_short_position(p.symbol) if not self.is_test else print(p.get_quantity(1)), p.update
                        else:
                            self.create_long_position(p.symbol) if not self.is_test else print(p.get_quantity(1)), p.update

                    self.threshold = -4
                    self.done = [False, False, False, False]
                    self.check_list = ["", "", "", ""]
                elif p.roi > 4 and not self.done[0]:
                    self.threshold = 2
                    self.done[0] = True
                elif p.roi > 15 and not self.done[1]:
                    if p.side == Side.SHORT:
                        p.close_short_position(0.5) if not self.is_test else print(p.get_quantity(0.5)), p.update
                    elif p.side == Side.LONG:
                        p.close_long_position(0.5) if not self.is_test else print(p.get_quantity(0.5)), p.update
                    self.done[1] = True
                elif p.roi > 30 and not self.done[2]:
                    if p.side == Side.SHORT:
                        p.close_short_position(0.5) if not self.is_test else print(p.get_quantity(0.5)), p.update
                    elif p.side == Side.LONG:
                        p.close_long_position(0.5) if not self.is_test else print(p.get_quantity(0.5)), p.update
                    self.done[2] = True
                    self.threshold = 15
                elif p.roi >= 50 and not self.done[3]:
                    if p.side == Side.SHORT:
                        p.close_short_position(1) if not self.is_test else print(p.get_quantity(1)), p.update
                    elif p.side == Side.LONG:
                        p.close_long_position(1) if not self.is_test else print(p.get_quantity(1)), p.update
                    self.done[3] = True

                if stream.account_update:
                    self.balance_change = stream.account_update[0]
                    self.balance = stream.account_update[1]
                    p.update()
                for index in range(len(self.done)):
                    if self.done[index] is True:
                        if self.check_list[index] == "":
                            self.check_list.insert(index, "*")
                callback([
                    p.pnl,
                    p.roi,
                    self.balance,
                    p.symbol,
                    str.join("", self.check_list)
                ])
                time.sleep(0.5)
            time.sleep(0.5)

    def set_test_position(self, symbol):
        stream.run_socket(symbol)
        while stream.streams[symbol]['currentCandle'].close == 0.0:
            time.sleep(0.5)
        pos = Position()
        pos.pos_amt = 7
        pos.entry_price = stream.streams[symbol]['currentCandle'].close
        pos.side = Side.LONG
        pos.symbol = symbol
        pos.leverage = 40
        pos.bep = pos.entry_price
        pos.margin = abs(pos.pos_amt) * pos.entry_price / pos.leverage
        self.positions[symbol] = pos
        t = threading.Thread(target=self._position_listener, args=(handle_position_listener, self.positions[symbol],))
        t.start()

    # CLIENT FUNCTIONS

    def set_quantity(self, ratio, symbol):
        quantity = 0.0
        res_margin = 0.0
        if ratio == 0.0:
            res_margin = 5.1
            min_q = res_margin / stream.streams[symbol]["currentCandle"].close
            return math.ceil(min_q * 10) / 10
        while res_margin < ratio * (self.balance * self.positions[symbol].leverage - (self.balance * self.positions[symbol].leverage) * 0.001):
            quantity += self.positions[symbol].min_qty()
            res_margin = quantity * stream.streams[symbol]["currentCandle"].close
        return quantity

    def create_short_position(self, symbol):
        stream.client.futures_change_leverage(symbol=symbol, leverage=self.positions[symbol].leverage)
        try:
            stream.client.futures_create_order(
                symbol=symbol,
                type='MARKET',
                side='SELL',
                quantity=self.set_quantity(0.5, symbol)
            )
            tz_turkey = pytz.timezone('Europe/Istanbul')
            datetime_turkey = datetime.now(tz_turkey)
            current_time = datetime_turkey.strftime("%H:%M:%S")
            print(f"\rSHORT: {stream.streams[symbol]["currentCandle"].close}", current_time)
            logging.info(current_time)
            self.positions[symbol].side = Side.SHORT
        except BinanceAPIException as err:
            if err.code == -2019:
                print(err.message)
                logging.error(err.message)
                raise BinanceAPIException(err.response, err.status_code, err.message)
            else:
                logging.exception('Create short exception occured:')
                raise BinanceAPIException(err.response, err.status_code, err.message)

    def create_long_position(self, symbol):
        stream.client.futures_change_leverage(symbol=symbol, leverage=self.positions[symbol].leverage)
        try:
            stream.client.futures_create_order(
                symbol=symbol,
                type='MARKET',
                side='BUY',
                quantity=self.set_quantity(0.5, symbol)
            )
            tz_turkey = pytz.timezone('Europe/Istanbul')
            datetime_turkey = datetime.now(tz_turkey)
            current_time = datetime_turkey.strftime("%H:%M:%S")
            print(f"\rLONG: {stream.streams[symbol]["currentCandle"].close}", current_time)
            logging.info(current_time)
            self.positions[symbol].side = Side.LONG
        except BinanceAPIException as err:
            if err.code == -2019:
                print(err.message)
                logging.error(err.message)
                raise BinanceAPIException(err.response, err.status_code, err.message)
            else:
                logging.exception('Create long exception occured:')
                raise BinanceAPIException(err.response, err.status_code, err.message)


class Status(Enum):
    LONG_ENTERING = auto()
    SHORT_ENTERING = auto()
    LONG_CLOSING = auto()
    SHORT_CLOSING = auto()
    LONG_SIGNAL = auto()
    SHORT_SIGNAL = auto()


class Tracker:
    def __init__(self):
        self._client = stream.client
        self._twm: ThreadedWebsocketManager = stream.twm
        self._streams = []
        self._running = True

    def run_loop(self):
        self.screaner()
        while self._running:
            time.sleep(0.5)

    def start_tracker(self):
        with open('streams.txt', 'r') as f:
            for line in f:
                line = line.replace('\n', '')
                self._streams.append(line)
        for _stream in self._streams:
            stream.run_socket(_stream)
        self.run_loop()

    def stop_tracker(self):
        self._running = False

    def screaner(self):
        while True:
            to_print = ""
            for s in stream.streams:
                to_print += (
                    f"\r{s}>> "
                    f"Price: {stream.streams[s]['currentCandle'].close}, "
                    f"Side: {side_checker(stream.streams[s])}"
                    # f"FE: {stream.streams[s]['fast_ema'][-1]:.5f}, "
                    # f"SE: {stream.streams[s]['slow_ema'][-1]:.5f}, "
                    # f"VSE: {stream.streams[s]['very_slow_ema'][-1]:.5f}"
                    # f"\n"
                )
            # os.system('cls')
            print(to_print, end="")
            # time.sleep(0.2)


def handle_position_listener(msg):
    print(f"\r{msg[3]}>> "
          f"Pnl: {msg[0]:.2f}, "
          f"Roi: {msg[1]:.2f}, "
          f"Balance: {msg[2]:.2f}, "
          f"{msg[4]} ", end="", flush=True)


def test():
    acc = Account()
    # tr = Tracker()
    # tr.start_tracker()


if __name__ == "__main__":
    test()

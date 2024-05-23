"""
Custom Binance Api

WARNING! Make sure to add 'BINANCE_API_KEY' and 'BINANCE_SECRET_KEY' variables to your system or user PATH before
start this script.

Communicates with Binance endpoints
"""

# TODO: prevent starting before other streams initialized

import pprint
from copy import deepcopy
import sys
import os
import logging
import threading
from threading import Lock
import time
from typing import List
import numpy as np
import pandas as pd
from talib import EMA

from binance import Client, ThreadedWebsocketManager
from binance.enums import HistoricalKlinesType, KLINE_INTERVAL_3MINUTE, FuturesType, ContractType

from utils.helpers import hist


class Candle:
    def __init__(self):
        self.timestamp: float = 0
        self.open: float = 0.0
        self.high: float = 0.0
        self.low: float = 0.0
        self.close: float = 0.0

    def __hash__(self):
        return hash((self.timestamp, self.open, self.high, self.low, self.close))

    def __eq__(self, other):
        return self.timestamp == other \
            and self.open == other \
            and self.high == other \
            and self.low == other \
            and self.close == other


class BinanceStreamManager:
    def __init__(self):
        self.account_update = []  # entry, quantity, commission
        self.account = None
        self.stream_name = None
        self.twm = None
        self.client: Client = Client()
        self._API_KEY = os.environ['BINANCE_API_KEY']
        self._SECRET_KEY = os.environ['BINANCE_SECRET_KEY']
        self.STARTTIME = '24 hour ago UTC'
        self.INTERVAL = KLINE_INTERVAL_3MINUTE
        self.SYMBOL = "DYDXUSDT"
        self.FAST_EMA = 7
        self.SLOW_EMA = 25
        self.VERY_SLOW_EMA = 99
        self.data: List[Candle] = []
        self.current_candle: Candle = Candle()
        self.interval_candle: Candle = Candle()
        self.streams = {}
        self._is_connected = True
        self.lock = Lock()
        self.connect()

    def connect(self):
        self.client = None
        step = 0
        while not self.client:
            try:
                self.client = Client(api_key=self._API_KEY, api_secret=self._SECRET_KEY,
                                     session_params={"trust_env": "True"})
                # self._init_data()
                self._is_connected = True
                t = threading.Thread(target=self.start_restart_listener)
                t.start()
                step = 0
            except Exception as e:
                logging.debug(f"[CONNECTION FAILED]: {e}")
                logging.debug(f"{e.args}")
                step += 1
                if step == 1:
                    print("Connection failed, waiting for reconnect: check your internet connection")
                time.sleep(5)
                continue

        logging.debug("CONNECTED")
        print("Connected to Binance")

    def start(self):
        try:
            self.twm = ThreadedWebsocketManager(api_key=self._API_KEY, api_secret=self._SECRET_KEY,
                                                session_params={"trust_env": "True"})
            self.twm.start()
            # self.stream_name = self.twm.start_kline_futures_socket(self.handle_socket_message, self.SYMBOL,
            #                                                        self.INTERVAL,
            #                                                        FuturesType.USD_M, ContractType.PERPETUAL)
            # self.run_socket(self.SYMBOL)
            self.account = self.twm.start_futures_user_socket(self.handle_futures_user_socket)
        except Exception as e:
            logging.debug(f"[STREAM FAILED]: {e}")
            logging.debug(f"{e.args}")
            sys.exit(1)
        logging.debug("STREAMING")
        print("Streaming started")

    def run_socket(self, symbol):
        self.stream_name = self.twm.start_kline_futures_socket(self.handle_socket_message, symbol,
                                                               self.INTERVAL,
                                                               FuturesType.USD_M, ContractType.PERPETUAL)
        self.streams[symbol] = {
            "currentCandle": Candle(),
            "intervalCandle": Candle(),
            "data": List[Candle],
            "fast_ema": list,
            "slow_ema": list,
            "very_slow_ema": list,
            "hist": list,
            "status": int
        }
        self._init_data(symbol)

    def stop(self):
        self.twm.stop()
        print("Streaming closed")

    def _init_data(self, symbol):
        data = []
        close = []
        close_array = np.array(1)
        historical_data = self.get_data_frame(symbol)
        for lineIndex in range(len(historical_data)):
            candle = Candle()
            candle.timestamp = float(historical_data['date'][lineIndex]) / 1000.0
            candle.open = float(historical_data['open'][lineIndex])
            candle.high = float(historical_data['high'][lineIndex])
            candle.low = float(historical_data['low'][lineIndex])
            candle.close = float(historical_data['close'][lineIndex])
            data.append(candle)
            close.append(candle.close)
            close_array = np.array(close)
        self.streams[symbol]["data"] = data
        self.streams[symbol]["close"] = close
        self.streams[symbol]["fast_ema"] = list(EMA(close_array, self.FAST_EMA))
        self.streams[symbol]["slow_ema"] = list(EMA(close_array, self.SLOW_EMA))
        self.streams[symbol]["very_slow_ema"] = list(EMA(close_array, self.VERY_SLOW_EMA))
        self.streams[symbol]["hist"] = hist(list(EMA(close_array, self.VERY_SLOW_EMA)))
        # self.data.append(candle)

    def start_restart_listener(self):
        sec_past = 0
        while self._is_connected:
            time.sleep(1)
            sec_past += 1
            if sec_past == 3500:
                self.client.futures_stream_keepalive(self.client.futures_stream_get_listen_key())
                self.client.stream_keepalive(self.client.stream_get_listen_key())
                sec_past = 0
        self.connect()
        self.start()
        for stream in self.streams:
            self.run_socket(stream)

    def handle_futures_user_socket(self, msg):
        # pprint.pprint(msg)
        if msg['e'] == 'ACCOUNT_UPDATE' and msg['a']['m'] == 'ORDER':
            self.account_update = [
                float(msg['a']['B'][0]['bc']),  # balance change
                float(msg['a']['B'][0]['wb']),  # balance
                float(msg['a']['P'][0]['bep']),  # bep
                float(msg['a']['P'][0]['ep']),  # entry price
                float(msg['a']['P'][0]['pa']),  # position amount
                str(msg['a']['P'][0]['s'])  # symbol
            ]

    def handle_socket_message(self, msg):
        # self.lock.acquire()
        if msg['e'] == 'error':
            print(f"{msg['m']}")
            self.twm.stop()
            self._is_connected = False

        elif bool(msg['k']['x']):
            self.current_candle.timestamp = float(msg['E']) // 1000
            self.current_candle.open = float(msg['k']['o'])
            self.current_candle.high = float(msg['k']['h'])
            self.current_candle.low = float(msg['k']['l'])
            self.current_candle.close = float(msg['k']['c'])
            self.streams[msg['ps']]['currentCandle'] = deepcopy(self.current_candle)

            self.streams[msg['ps']]['data'].pop(0)
            self.streams[msg['ps']]['data'].append(deepcopy(self.current_candle))

            self.streams[msg['ps']]['close'].pop(0)
            self.streams[msg['ps']]['close'].append(deepcopy(self.current_candle.close))

            self.streams[msg['ps']]['fast_ema'] = list(EMA(np.array(self.streams[msg['ps']]['close']), self.FAST_EMA))
            self.streams[msg['ps']]['slow_ema'] = list(EMA(np.array(self.streams[msg['ps']]['close']), self.SLOW_EMA))
            self.streams[msg['ps']]['very_slow_ema'] = list(EMA(np.array(self.streams[msg['ps']]['close']), self.VERY_SLOW_EMA))
            self.streams[msg['ps']]["hist"] = hist(list(EMA(np.array(self.streams[msg['ps']]['close']), self.VERY_SLOW_EMA)))
        else:
            self.current_candle.timestamp = float(msg['E']) // 1000
            self.current_candle.open = float(msg['k']['o'])
            self.current_candle.high = float(msg['k']['h'])
            self.current_candle.low = float(msg['k']['l'])
            self.current_candle.close = float(msg['k']['c'])
            self.streams[msg['ps']]['currentCandle'] = deepcopy(self.current_candle)
        # self.lock.release()

    def get_data_frame(self, pair):
        """
        Returns historical klines in DataFrame format from Binance within certain interval of time.

        return format: pd.Dataframe["date", "open", "high", "low", "close"]

        valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M request historical candle (or
        klines) data using timestamp from above, interval either every min, hr, day or month

        starttime = '30 minutes ago UTC' for last 30 mins time
        e.g. client.get_historical_klines(symbol='ETHUSDT', '1m', starttime)

        starttime = '1 Dec, 2017', '1 Jan, 2018'  for last month of 2017
        e.g. client.get_historical_klines(symbol='BTCUSDT', '1h', "1 Dec, 2017", "1 Jan, 2018")

        :return historical data: pd.Dataframe
        """

        bars = self.client.get_historical_klines(symbol=pair, contract_type=ContractType.PERPETUAL,
                                                 interval=self.INTERVAL,
                                                 start_str=self.STARTTIME,
                                                 klines_type=HistoricalKlinesType.FUTURES_PERP)

        for line in bars:  # Keep only first 5 columns, "date" "open" "high" "low" "close"
            del line[5:]
        df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])  # 2 dimensional tabular data
        return df


def test():
    stream = BinanceStreamManager()
    stream.start()
    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    logging.basicConfig(filename=".log.txt",
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    test()

# long buy response to user socket
"""{'E': 1715366650776,
 'T': 1715366650776,
 'e': 'ORDER_TRADE_UPDATE',
 'o': {'L': '0',
       'N': 'USDT',
       'R': False,
       'S': 'BUY',
       'T': 1715366650776,
       'V': 'NONE',
       'X': 'NEW',
       'a': '0',
       'ap': '0',
       'b': '0',
       'c': 'ios_FlPqUnoWJ8HRDNMUZMpY',
       'cp': False,
       'f': 'GTC',
       'gtd': 0,
       'i': 13840358870,
       'l': '0',
       'm': False,
       'n': '0',
       'o': 'MARKET',
       'ot': 'MARKET',
       'p': '0',
       'pP': False,
       'pm': 'NONE',
       'ps': 'BOTH',
       'q': '2.5',
       'rp': '0',
       's': 'DYDXUSDT',
       'si': 0,
       'sp': '0',
       'ss': 0,
       't': 0,
       'wt': 'CONTRACT_PRICE',
       'x': 'NEW',
       'z': '0'}}
{'E': 1715366650776,
 'T': 1715366650776,
 'a': {'B': [{'a': 'USDT', 'bc': '0', 'cw': '5.98046928', 'wb': '5.98046928'}],
       'P': [{'bep': '2.0400195',
              'cr': '-11.01329954',
              'ep': '2.039',
              'iw': '0',
              'ma': 'USDT',
              'mt': 'cross',
              'pa': '2.5',
              'ps': 'BOTH',
              's': 'DYDXUSDT',
              'up': '-0.00063850'}],
       'm': 'ORDER'},
 'e': 'ACCOUNT_UPDATE'}
{'E': 1715366650776,
 'T': 1715366650776,
 'e': 'ORDER_TRADE_UPDATE',
 'o': {'L': '2.039',
       'N': 'USDT',
       'R': False,
       'S': 'BUY',
       'T': 1715366650776,
       'V': 'NONE',
       'X': 'FILLED',
       'a': '0',
       'ap': '2.0390',
       'b': '0',
       'c': 'ios_FlPqUnoWJ8HRDNMUZMpY',
       'cp': False,
       'f': 'GTC',
       'gtd': 0,
       'i': 13840358870,
       'l': '2.5',
       'm': False,
       'n': '0.00254874',
       'o': 'MARKET',
       'ot': 'MARKET',
       'p': '0',
       'pP': False,
       'pm': 'NONE',
       'ps': 'BOTH',
       'q': '2.5',
       'rp': '0',
       's': 'DYDXUSDT',
       'si': 0,
       'sp': '0',
       'ss': 0,
       't': 453276325,
       'wt': 'CONTRACT_PRICE',
       'x': 'TRADE',
       'z': '2.5'}}
"""

# long sell response to user socket
"""{'E': 1715366742956,
 'T': 1715366742956,
 'e': 'ORDER_TRADE_UPDATE',
 'o': {'L': '0',
       'N': 'USDT',
       'R': True,
       'S': 'SELL',
       'T': 1715366742956,
       'V': 'NONE',
       'X': 'NEW',
       'a': '0',
       'ap': '0',
       'b': '0',
       'c': 'ios_d2wmUzIgdqHYPTj9vgyn',
       'cp': False,
       'f': 'GTC',
       'gtd': 0,
       'i': 13840367820,
       'l': '0',
       'm': False,
       'n': '0',
       'o': 'MARKET',
       'ot': 'MARKET',
       'p': '0',
       'pP': False,
       'pm': 'NONE',
       'ps': 'BOTH',
       'q': '2.5',
       'rp': '0',
       's': 'DYDXUSDT',
       'si': 0,
       'sp': '0',
       'ss': 0,
       't': 0,
       'wt': 'CONTRACT_PRICE',
       'x': 'NEW',
       'z': '0'}}
{'E': 1715366742956,
 'T': 1715366742956,
 'a': {'B': [{'a': 'USDT', 'bc': '0', 'cw': '5.96292803', 'wb': '5.96292803'}],
       'P': [{'bep': '0',
              'cr': '-11.02829954',
              'ep': '0',
              'iw': '0',
              'ma': 'USDT',
              'mt': 'cross',
              'pa': '0',
              'ps': 'BOTH',
              's': 'DYDXUSDT',
              'up': '0'}],
       'm': 'ORDER'},
 'e': 'ACCOUNT_UPDATE'}
{'E': 1715366742956,
 'T': 1715366742956,
 'e': 'ORDER_TRADE_UPDATE',
 'o': {'L': '2.033',
       'N': 'USDT',
       'R': True,
       'S': 'SELL',
       'T': 1715366742956,
       'V': 'NONE',
       'X': 'FILLED',
       'a': '0',
       'ap': '2.0330',
       'b': '0',
       'c': 'ios_d2wmUzIgdqHYPTj9vgyn',
       'cp': False,
       'f': 'GTC',
       'gtd': 0,
       'i': 13840367820,
       'l': '2.5',
       'm': False,
       'n': '0.00254125',
       'o': 'MARKET',
       'ot': 'MARKET',
       'p': '0',
       'pP': False,
       'pm': 'NONE',
       'ps': 'BOTH',
       'q': '2.5',
       'rp': '-0.01500000',
       's': 'DYDXUSDT',
       'si': 0,
       'sp': '0',
       'ss': 0,
       't': 453276596,
       'wt': 'CONTRACT_PRICE',
       'x': 'TRADE',
       'z': '2.5'}}
"""

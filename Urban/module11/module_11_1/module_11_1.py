"""
Custom Binance Manager

WARNING!!!
    Was used outdated 'python-binance' library. Some changes have been made to make it work.
Run setup.py first to make this magic work :)'
    Make sure to add 'BINANCE_API_KEY' and 'BINANCE_SECRET_KEY' variables to your system or user PATH before
 starting this script.

Communicates with Binance Api endpoints via 'python-binance' library. Fetches by default BTCUSDT pairs close
price for last hour interval, finds maximum price and plots it on a graph.
"""
import datetime
import os

import pandas as pd
import matplotlib.pyplot as plt
from binance import Client
from binance.enums import HistoricalKlinesType, KLINE_INTERVAL_3MINUTE, ContractType


class BinanceManager:
    def __init__(self):
        self._API_KEY = os.environ['BINANCE_API_KEY']
        self._SECRET_KEY = os.environ['BINANCE_SECRET_KEY']
        self.client = Client(api_key=self._API_KEY, api_secret=self._SECRET_KEY)
        self.SYMBOL = "BTCUSDT"
        self.STARTTIME = '1 hour ago UTC'
        self.INTERVAL = KLINE_INTERVAL_3MINUTE
        print("Connected to Binance")

    def get_historical_data_frame(self):
        """
        Returns historical klines in DataFrame format from Binance within a certain interval of time.

        Return format: pd.Dataframe["date", "open", "high", "low", "close"]

        valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M request historical candle (or
        klines) data using timestamp from above, interval either every min, hr, day or month

        Starttime = '30 minutes ago UTC' for last 30 mins time
        e.g., client.get_historical_klines(symbol='ETHUSDT', '1m', starttime)

        Starttime = '1 Dec, 2017', '1 Jan, 2018' for last month of 2017
        e.g. client.get_historical_klines(symbol='BTCUSDT', '1h', "1 Dec, 2017", "1 Jan, 2018")

        :return historical data: Pd.Dataframe
        """

        bars = self.client.get_historical_klines(symbol=self.SYMBOL,
                                                 interval=self.INTERVAL,
                                                 start_str=self.STARTTIME,
                                                 klines_type=HistoricalKlinesType.SPOT,
                                                 contract_type=ContractType.PERPETUAL)

        for line in bars:  # Keep only the first 5 columns, "date" "open" "high" "low" "close"
            del line[5:]
        df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])  # 2 dimensional tabular data
        return df


bm = BinanceManager()
data: pd.DataFrame = bm.get_historical_data_frame()

# convert date data to valid timestamp
date = []
for lineIndex in range(len(data)):
    ts = float(data['date'][lineIndex]) // 1000  # delete milliseconds
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
    date.append(timestamp)

# print dataframe data
print("Historical data within a hour:")
print(data)

# fetch 'close' prices as numpy of a float type
close = data["close"].to_numpy(dtype=float)
plt.plot(date, close)  # plot graph

# some numpy functionality
max_price = close.max()
max_index = close.argmax()
print("Max close price within a hour:", max_price)

# some matplotlib functionality
plt.plot(max_index, max_price, 'ro', label=f'Max Value {max_price}')
plt.title(f"{bm.SYMBOL} graph with {bm.INTERVAL} interval started {bm.STARTTIME}")
plt.xlabel("Time")
plt.ylabel(f"{bm.SYMBOL} price")
plt.legend()
plt.show()

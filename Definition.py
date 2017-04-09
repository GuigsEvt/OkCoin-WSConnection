import os, CryptoBLL

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_CONFIG_INI = 'InitFiles/config.ini'

CANDLESTICK_1 = CryptoBLL.TIMEFRAME.FOUR_HOUR

CANDLESTICK_2 = CryptoBLL.TIMEFRAME.TWELVE_HOUR

CANDLESTICK_3 = CryptoBLL.TIMEFRAME.ONE_DAY

DATABASE_TRADING = 'Trading'

DATABASE_ARBITRAGE = 'Arbitrage'
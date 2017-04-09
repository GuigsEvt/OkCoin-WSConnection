import datetime
import CryptoBLL
from enum import Enum

class Candlestick(object):

    def __init__(self, open, high, low, close, volume, time, timeframe):
        self.open = str(float(open))
        self.high = str(float(high))
        self.low = str(float(low))
        self.close = str(float(close))
        self.volume = str(float(volume))
        self.time = time
        self.timeframe = timeframe

    def toJSON(self):
        #if isinstance(self.time, int):
        return { 'timeframe' : self.timeframe,
                    'time' : str(datetime.datetime.fromtimestamp(int(self.time)).strftime('%Y-%m-%d %H:%M:%S')),
                    'open' : self.open,
                    'high' : self.high,
                    'low' : self.low,
                    'close' : self.close,
                    'volume' : self.volume
                    }

class TIMEFRAME(Enum):
    ONE_MIN = '1min'
    THREE_MIN = '3min'
    FIVE_MIN = '5min'
    FIFTEEN_MIN = '15min'
    THIRTY_MIN = '30min'
    ONE_HOUR = '1hour'
    TWO_HOUR = '2hour'
    FOUR_HOUR = '4hour'
    SIX_HOUR = '6hour'
    TWELVE_HOUR = '12hour'
    ONE_DAY = 'day'
    THREE_DAY = '3day'
    ONE_WEEK = 'week'
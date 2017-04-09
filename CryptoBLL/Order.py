import datetime
import CryptoBLL

from enum import Enum

class Order(object) :

    def __init__(self, exchange, pair, side, orderType, price, volume) :
        if exchange not in CryptoBLL.Factory.exchange:
            raise Exception()
        if pair not in CryptoBLL.Pairs[exchange].values():
            raise Exception()
        if float(price) < 0:
            raise Exception()
        if float(volume) <= 0:
            raise Exception()
        if side not in ORDERSIDE:
            raise Exception()
        if orderType not in ORDERTYPE:
            raise Exception()

        self.exchange = exchange
        self.pair = pair
        self.side = side
        self.orderType = orderType
        self.orderState = ORDERSTATE.SUBMITTED
        self.price = price
        self.volume = volume
        self.__volume = volume
        self.executedVolume = 0
        self.timestampCreation = str(datetime.datetime.now())
        self.timestampEnd = None
        self.id = None
        self.pairingOrders = []

    def setId(self, id):
        self.id = str(id)
        self.orderState = ORDERSTATE.ACCEPTED

    def addPairedOrders(self, ids):
        self.pairingOrders.append(ids)

    def setState(self, newState):
        if newState == ORDERSTATE.FILLED:
            self.timestampEnd = str(datetime.datetime.now())
            self.executedVolume = self.volume
        self.orderState = newState

    # Use for logging for arbitrage strategy
    def toJSON(self):
        return {        'Exchange' : self.exchange,
                        'Pair' : self.pair,
                        'Type' : self.side.value,
                        'OrderType' : self.orderType.value,
                        'Price' : self.price,
                        'Executed_Volume' : self.executedVolume,
                        'Volume' : self.__volume,
                        'Corresponding orders' : self.pairingOrders,
                        'Timestamp_Creation' : self.timestampCreation,
                        'TImestamp_End' : self.timestampEnd,
                        'State' : self.orderState.value,
                        'Id' : self.id}

    # Use for logging for trading strategy
    def toTrading(self):
        return [{'Side' : self.side.value,
                 'Price' : self.price,
                 'Vol' : self.__volume,
                 'ExcVol' : self.executedVolume,
                 'TimeStamp' : self.timestampCreation,
                 'State' : self.orderState.value}]


### ENUM for side, type and state of the order. Must be use in all cases. --------------------------------------------------------------

class ORDERSIDE(Enum):
    BUY = 'buy'
    SELL = 'sell'

class ORDERTYPE(Enum):
    #MARKET = 'market'
    LIMIT = 'limit'
    #STOP_LOSS = 'stop loss'
    #TAKE_PROFIT = 'take profit'

class ORDERSTATE(Enum):
    SUBMITTED = 'Initiated'
    ACCEPTED = 'Accepted'
    CANCELED = 'Canceled'
    PARTIALLY_FILLED = 'Partially filled'
    FILLED = 'Filled'
    CLOSED = 'Closed'
    UNKNOWN = 'Unknown'

# Must be use later when we will use Order for trading as well
class ORDERMODULE(Enum):
    ARBITRAGE = 1
    TRADING = 2

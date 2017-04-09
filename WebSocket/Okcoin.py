import WebSocket.websocket
import CryptoBLL, Definition
import sys, json, zlib, hashlib, threading, time, datetime
from WebSocket.websocket import create_connection
from collections import deque
import MongoDB
#from dateutil.relativedelta import relativedelta


class Okcoin(object):

    def __init__(self, api_key, secret_key, uri):
        self.api_key = api_key
        self.secret_key = secret_key
        self.uri = uri
        # Create websocket to add and cancel orders
        self.ws = create_connection(self.uri)

        # Duplicate object for the threading channel
        WebSocket.Okcoin.instance = self

        # Threading to run separetely the run_forever function of the websocket aimed to retrieve market data
        thread = threading.Thread(target=self.run)
        thread.daemon = True  # Daemonize thread - it allows the main application to exit even if the thread is still running
        thread.start()

        # Instance of mongoDb database to log trades and candlesticks
        self.mongo = MongoDB.MongoDB()
        self.initObject()

    def initObject(self):
        # Trading object - For each new most left is going out and each one is swaping to the left
        self.trades = deque(maxlen=100)
        self.listIdTrades = deque(maxlen=100)
        self.trades = self.recoverTradesFromDatabase()
        self.candleStick1 = deque(maxlen=100)
        self.candleStick1 = self.recoverCandlesticksFromDatabase({'timeframe' : Definition.CANDLESTICK_1.value })
        self.candleStick2 = deque(maxlen=100)
        self.candleStick2 = self.recoverCandlesticksFromDatabase({'timeframe' : Definition.CANDLESTICK_2.value })
        self.candleStick3 = deque(maxlen=100)
        self.candleStick3 = self.recoverCandlesticksFromDatabase({'timeframe' : Definition.CANDLESTICK_3.value })

    def run(self):
        # Websocket object aimed to retrieve market data continously
        WebSocket.websocket.enableTrace(False)
        if len(sys.argv) < 2:
            host = self.uri
        else:
            host = sys.argv[1]
        self.ws = WebSocket.websocket.WebSocketApp(host,
                                                   on_message=on_message,
                                                   on_error=on_error,
                                                   on_close=on_close)
        self.ws.on_open = on_open
        self.ws.run_forever()


    def reconnectWebsocket(self):
        self.ws.close()
        self.initObject()
        self.run()
        return

    def buildMySign(self, params, secret):
        sign = ''
        for key in sorted(params.keys()):
            sign += key + '=' + str(params[key]) + '&'
        return hashlib.md5((sign + 'secret_key=' + secret).encode("utf-8")).hexdigest().upper()

    def inflate(self, data):

        decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        inflated = inflated.decode("utf-8")
        inflated = inflated[1:-1]
        nbEvent = inflated.count('"channel"')
        #print (nbEvent)
        #print(str(inflated))
        if nbEvent == 1:
            return [json.loads(inflated)]
        else:
            eventAsDict = '[' + inflated + ']'
            eventAsJSON = json.loads(eventAsDict)
            return eventAsJSON
            #events = []
            #for event in eventAsJSON:
            #    print (str(event))
            #    events.append(json.loads(event))

    def getName(self):
        return 'Okcoin'

# CHANNEL REQUEST-----------------------------------------

    def addOrder(self, order):
        params = {
            'api_key': self.api_key,
            'symbol': str(order.pair),
            'type': order.side.value,
            'price' : str(order.price),
            'amount' : str(order.volume)
        }
        sign = self.buildMySign(params, self.secret_key)
        dataToSend = "{'event':'addChannel','channel':'ok_spotusd_trade','parameters':{'api_key':'" + self.api_key + "',\
                'sign':'" + sign + "','symbol':'" + str(order.pair) + "','type':'" + order.side.value + "','price':'" + str(order.price) + "',\
                'amount':'" + str(order.volume) + "'},'binary':'true'}"
        self.ws.send(dataToSend)
        result = self.ws.recv()
        result = self.inflate(result)
        try:
            if bool(result['data']['result']):
                order.setId(result['data']['order_id'])
                CryptoBLL.Logger.LogInfo('Order added successfully: ' + str(result['data']['order_id']), self.__class__.__name__)
                return True
            else:
                CryptoBLL.Logger.LogError('Order not sent error number: ' + str(result['errorcode']), self.__class__.__name__)
                order.setState(CryptoBLL.ORDERSTATE.CANCELED)
                return False
        except:
            CryptoBLL.Logger.LogError('Order not sent error number: ' + str(result['errorcode']), self.__class__.__name__)
            order.setState(CryptoBLL.ORDERSTATE.CANCELED)
            return False

    def cancelOrder(self, order):
        if not order.id:
            CryptoBLL.Logger.LogError('Deletion canceled: no order id in the object', self.__class__.__name__)
            return False
        params = {
        'api_key': self.api_key,
        'symbol': str(order.pair),
        'order_id': str(order.id)
        }
        sign = self.buildMySign(params,self.secret_key)
        dataToSend = "{'event':'addChannel','channel': 'ok_spotusd_cancel_order','parameters':{'api_key':'"+self.api_key+"','sign':'"+sign+"',\
            'symbol':'"+str(order.pair)+"','order_id':'"+str(order.id)+"'},'binary':'true'}"
        self.ws.send(dataToSend)
        result = self.ws.recv()
        result = self.inflate(result)
        try:
            if bool(result['data']['result']):
                order.setState(CryptoBLL.ORDERSTATE.CANCELED)
                CryptoBLL.Logger.LogInfo('Deletion completed for order: ' + str(order.id), self.__class__.__name__)
                return True
            else:
                CryptoBLL.Logger.LogError('Deletion canceled error number: ' + str(result['errorcode']), self.__class__.__name__)
                return False
        except:
            CryptoBLL.Logger.LogError('Deletion canceled error number: ' + str(result['errorcode']), self.__class__.__name__)
            return False

    def updateOrders(self):
        params = {'api_key': self.api_key}
        sign = self.buildMySign(params, self.secret_key)
        return "{'event':'addChannel','channel':'ok_sub_spotusd_trades','parameters':{'api_key':'" + self.api_key + "','sign':'" + sign + "'},'binary':'true'}"

    #def updateTradingObject(self, object):

    def updateTradesList(self, trades):
        for trade in trades:
            if not trade.id in self.listIdTrades:
                self.trades.append(trade)
                self.listIdTrades.append(trade.id)
                self.mongo.addDocument(trade, MongoDB.COLLECTIONS.TRADE)

    def updateCandleStickList(self, candlesticks):
        if candlesticks[0].timeframe == Definition.CANDLESTICK_1.value:
            if len(self.candleStick1) > 0:
                for candlestick in candlesticks:
                    if candlestick.time == self.candleStick1[-1].time:
                        self.candleStick1[-1] = candlestick
                        self.mongo.updateDocument(MongoDB.COLLECTIONS.CANDLESTICK, candlestick, { 'time' : str(datetime.datetime.fromtimestamp(int(candlestick.time)).strftime('%Y-%m-%d %H:%M:%S')),
                                                                                                  'timeframe' : candlestick.timeframe})
                    elif candlestick.time < self.candleStick1[-1].time:
                        return
                    else:
                        self.candleStick1.append(candlestick)
                        self.mongo.addDocument(candlestick, MongoDB.COLLECTIONS.CANDLESTICK)
            else:
                for candlestick in candlesticks:
                    print (str(candlestick.toJSON()))
                    self.candleStick1.append(candlestick)
                    self.mongo.addDocument(candlestick, MongoDB.COLLECTIONS.CANDLESTICK)
        elif candlesticks[0].timeframe == Definition.CANDLESTICK_2.value:
            if len(self.candleStick2) > 0:
                for candlestick in candlesticks:
                    if candlestick.time == self.candleStick2[-1].time:
                        self.candleStick2[-1] = candlestick
                        self.mongo.updateDocument(MongoDB.COLLECTIONS.CANDLESTICK, candlestick, {'time': str(
                            datetime.datetime.fromtimestamp(int(candlestick.time)).strftime('%Y-%m-%d %H:%M:%S')),
                                                                                                 'timeframe': candlestick.timeframe})
                    elif candlestick.time < self.candleStick2[-1].time:
                        return
                    else:
                        self.candleStick2.append(candlestick)
                        self.mongo.addDocument(candlestick, MongoDB.COLLECTIONS.CANDLESTICK)
            else:
                for candlestick in candlesticks:
                    self.candleStick2.append(candlestick)
                    self.mongo.addDocument(candlestick, MongoDB.COLLECTIONS.CANDLESTICK)
        elif candlesticks[0].timeframe == Definition.CANDLESTICK_3.value:
            if len(self.candleStick3) > 0:
                for candlestick in candlesticks:
                    if candlestick.time == self.candleStick3[-1].time:
                        self.candleStick3[-1] = candlestick
                        self.mongo.updateDocument(MongoDB.COLLECTIONS.CANDLESTICK, candlestick, {'time': str(
                            datetime.datetime.fromtimestamp(int(candlestick.time)).strftime('%Y-%m-%d %H:%M:%S')),
                                                                                                 'timeframe': candlestick.timeframe})
                    elif candlestick.time < self.candleStick3[-1].time:
                        return
                    else:
                        self.candleStick3.append(candlestick)
                        self.mongo.addDocument(candlestick, MongoDB.COLLECTIONS.CANDLESTICK)
            else:
                for candlestick in candlesticks:
                    self.candleStick3.append(candlestick)
                    self.mongo.addDocument(candlestick, MongoDB.COLLECTIONS.CANDLESTICK)

    def recoverTradesFromDatabase(self):
        tradesJSON = self.mongo.getDocument(MongoDB.COLLECTIONS.TRADE, 100, [('time', -1)])
        print ('Trades from database: ' + str(tradesJSON))
        trades = []
        for trade in reversed(list(tradesJSON)):
            trades.append(CryptoBLL.Trade(trade['id'], trade['price'], trade['amount'], trade['time'], trade['type']))
            self.listIdTrades.append(trade['id'])
        return trades

    def recoverCandlesticksFromDatabase(self, criteria):
        candlesJSON =  self.mongo.getDocumentOnCriteria(MongoDB.COLLECTIONS.CANDLESTICK, 100, criteria, [('time', -1)])
        print ('Candles from database: ' + str(candlesJSON))
        candles = []
        for candle in reversed(list(candlesJSON)):
            #print (str(candle))
            candles.append(CryptoBLL.Candlestick(candle['open'], candle['high'], candle['low'], candle['close'],
                                                 candle['volume'], time.mktime(datetime.datetime.strptime(candle['time'], '%Y-%m-%d %H:%M:%S').timetuple()),
                                                 candle['timeframe']))
        return candles

# EVENTS FOR CONTINUOUS CONTINUOUS WEBSOCKET-----------------------------------------

instance = None

def on_message(self,evt):
    data = instance.inflate(evt) #data decompress
    for event in data:
        print (str(event))
        channel = event['channel']
        print (str(channel))
        if channel == 'ok_sub_spotusd_btc_trades':
            if 'data' in event:
                trades = []
                for trade in event['data']:
                    #print (str(trade))
                    today = datetime.date.today()
                    dateTrade = datetime.datetime.strptime(str(trade[3]), "%H:%M:%S")
                    dateTradeOkcoin = datetime.datetime(today.year, today.month, today.day, dateTrade.hour, dateTrade.minute, dateTrade.second)
                    #dateTradeOkcoin += relativedelta(hours = -8)
                    print (dateTradeOkcoin)
                    trades.append(CryptoBLL.Trade(str(trade[0]), float(trade[1]), round(float((trade[2])), 3), dateTradeOkcoin, str(trade[4])))
                instance.updateTradesList(trades)
        elif channel == 'ok_sub_spotusd_btc_kline_'+  Definition.CANDLESTICK_1.value :
            if 'data' in event:
                candles = []
                if (isinstance(event['data'][0], list)):
                    for candlestick in list(event['data']):
                        candles.append(CryptoBLL.Candlestick(float(candlestick[1]), float(candlestick[2]), float(candlestick[3]),
                                                            float(candlestick[4]), float(candlestick[5]), (candlestick[0]/1000) - 3600,
                                                            Definition.CANDLESTICK_1.value))
                else:
                    candles.append(
                        CryptoBLL.Candlestick(float(event['data'][1]), float(event['data'][2]), float(event['data'][3]),
                                            float(event['data'][4]), float(event['data'][5]), (event['data'][0] / 1000) - 3600,
                                            Definition.CANDLESTICK_1.value))
                instance.updateCandleStickList(candles)
                print ('finish')
        elif channel == 'ok_sub_spotusd_btc_kline_' + Definition.CANDLESTICK_2.value:
            if 'data' in event:
                candles = []
                if (isinstance(event['data'][0], list)):
                    for candlestick in list(event['data']):
                        candles.append(CryptoBLL.Candlestick(float(candlestick[1]), float(candlestick[2]), float(candlestick[3]),
                                                            float(candlestick[4]), float(candlestick[5]), (candlestick[0]/1000) - 3600,
                                                            str(Definition.CANDLESTICK_2.value)))
                else:
                    candles.append(
                        CryptoBLL.Candlestick(float(event['data'][1]), float(event['data'][2]), float(event['data'][3]),
                                            float(event['data'][4]), float(event['data'][5]), (event['data'][0] / 1000) - 3600,
                                            str(Definition.CANDLESTICK_2.value)))
                instance.updateCandleStickList(candles)
        elif channel == 'ok_sub_spotusd_btc_kline_' + Definition.CANDLESTICK_3.value:
            if 'data' in event:
                candles = []
                if (isinstance(event['data'][0], list)):
                    for candlestick in list(event['data']):
                        candles.append(CryptoBLL.Candlestick(float(candlestick[1]), float(candlestick[2]), float(candlestick[3]),
                                                            float(candlestick[4]), float(candlestick[5]), (candlestick[0]/1000) - 3600,
                                                            str(Definition.CANDLESTICK_3.value)))
                else:
                    candles.append(
                        CryptoBLL.Candlestick(float(event['data'][1]), float(event['data'][2]), float(event['data'][3]),
                                            float(event['data'][4]), float(event['data'][5]), (event['data'][0] / 1000) - 3600,
                                            str(Definition.CANDLESTICK_3.value)))
                instance.updateCandleStickList(candles)

def on_error(self,evt):
    print ('Problem connecting to the network')
    while not (CryptoBLL.Utils.InternetConnection()):
        print ('No network connection. We cannot connect to Okcoin websocket.')
        time.sleep(30)
    if (instance.reconnectWebsocket()):
        print ('Reconnection to Websocket server done.')
    #CryptoBLL.Logger.LogError(evt)

def on_close(self):
    print('DISCONNECT')

def on_open(self):

    # Subscribe for okcoin spot trades
    self.send("{'event':'addChannel','channel':'ok_sub_spotusd_btc_trades','binary':'true'}");

    # Subscribe to receive updates on our trades -- note that no update is done for cancellation
    #self.send(instance.updateOrders())

    # Subscribe for candlesticks number 1
    self.send("{'event':'addChannel','channel':'ok_sub_spotusd_btc_kline_"+  Definition.CANDLESTICK_1.value + "','binary':'true'}");

    # Subscribe for candlesticks number 2
    self.send("{'event':'addChannel','channel':'ok_sub_spotusd_btc_kline_" + Definition.CANDLESTICK_2.value + "','binary':'true'}");

    # Subscribe for candlesticks number 3
    self.send("{'event':'addChannel','channel':'ok_sub_spotusd_btc_kline_" + Definition.CANDLESTICK_3.value + "','binary':'true'}");





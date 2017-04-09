import io, os, json, datetime
from Definition import ROOT_DIR
import CryptoBLL, Definition
from collections import OrderedDict

# File for arbitrage
ORDER_ARBITRAGE = (ROOT_DIR + '/JSON/Arbitrage/OrdersArbitrage/Orders_ArbitrageId_')
ARBITRAGE = (ROOT_DIR + '/JSON/Arbitrage/Arbitrage/Arbitrage_' + str(datetime.date.today()) + '.json')
BALANCES_ARBITRAGE = (ROOT_DIR + '/JSON/Arbitrage/Balance/Balance_Arbitrage.json')
LOGS = (ROOT_DIR + '/JSON/Arbitrage/Logs/Logs_' + str(datetime.date.today()) + '.txt')
LOGS_STATE = (ROOT_DIR + '/JSON/Arbitrage/Logs/LogsState.txt')

# File for trading
ORDERS_TRADING = (ROOT_DIR + '/JSON/Trading/Orders/Orders_' + str(datetime.date.today()) + '.json')
CANDLESTICK_1 = (ROOT_DIR + '/JSON/Trading/Candlestick/' + Definition.CANDLESTICK_1.value + '/' + str(datetime.date.today()) + '.json')
CANDLESTICK_2 = (ROOT_DIR + '/JSON/Trading/Candlestick/' + Definition.CANDLESTICK_2.value + '/' + str(datetime.date.today()) + '.json')
CANDLESTICK_3 = (ROOT_DIR + '/JSON/Trading/Candlestick/' + Definition.CANDLESTICK_3.value + '/' + str(datetime.date.today()) + '.json')
TRADES_TRADING = (ROOT_DIR + '/JSON/Trading/Trades/Trades_' + str(datetime.date.today()) + '.json')

class Logger(object):

#########################################################################################
############################# LOGS FOR ARBITRAGE PROCESS ################################
#########################################################################################

    @staticmethod
    def LogOrderArbitrage(order, arbitrage):
        file = ORDER_ARBITRAGE + str(arbitrage.id) + '.json'
        if not os.path.isfile(file):
            io.open(file, 'w', encoding='utf-8')
        Logger.UpdateJsonObject(file, str(datetime.datetime.now()) + ' ID:  ' + str(order.id), order)

    @staticmethod
    def LogBalance(balance):
        if not balance:
            return
        file = BALANCES_ARBITRAGE
        if not os.path.isfile(file):
            io.open(file, 'w', encoding='utf-8')
        Logger.WriteJson(file, 'Balance arbitrage ' + str(datetime.datetime.now().date()), balance)

    @staticmethod
    def LogArbitrage(arbitrage):
        file = ARBITRAGE
        if not os.path.isfile(file):
            io.open(file, 'w', encoding='utf-8')
        Logger.UpdateJsonObject(file, str(datetime.datetime.now()) + ' ID Arbitrage:  ' + str(arbitrage.id), arbitrage)

#########################################################################################
#########################################################################################
#########################################################################################

#########################################################################################
######################### LOGS FOR TRADING PROCESS ######################################
#########################################################################################


    @staticmethod
    def LogOrderTrading(order):
        file = ORDERS_TRADING
        if not os.path.isfile(file):
            io.open(file, 'w', encoding='utf-8')
        Logger.UpdateJsonObject(file, {'Order_Id' : order.id}, order)

    @staticmethod
    def UpdateOrderTradingFile():
        file = ORDERS_TRADING
        if not os.path.isfile(file):
            io.open(file, 'w', encoding='utf-8')
        yesterdayFile = (ROOT_DIR + '/JSON/Trading/OrdersBTCUSD/Orders_' + str(datetime.date.fromordinal(datetime.date.today().toordinal()-1)) + '.json')
        if not os.path.isfile(yesterdayFile):
            return
        if os.path.getsize(yesterdayFile) == 0:
            return
        else:
            with io.open(yesterdayFile) as f_read:
                data = dict(json.load(f_read))
                f_read.close()
            newData = {}
            dataToDelete = []
            for k,v in data.items():
                if v[0]['State'] in ['Accepted', 'Initiated', 'Partially filled']:
                    newData[k] = v
                    dataToDelete.append(k)
            if dataToDelete:
                for dataToDelete in dataToDelete:
                    del data[dataToDelete]
                with io.open(file, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))
                    f.write('\n')
                    f.flush()
                    f.close()
                with io.open(yesterdayFile, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(newData, ensure_ascii=False, sort_keys=True, indent=4))
                    f.write('\n')
                    f.flush()
                    f.close()

    @staticmethod
    def LogCandlestick(candlesticks, timeframe):
        print (str(candlesticks))
        if timeframe == Definition.CANDLESTICK_1:
            file = CANDLESTICK_1
        elif timeframe == Definition.CANDLESTICK_2:
            file = CANDLESTICK_2
        elif timeframe == Definition.CANDLESTICK_3:
            file = CANDLESTICK_3
        if not os.path.isfile(file):
            io.open(file, 'w', encoding='utf-8')
        if not isinstance(candlesticks, list):
            candlesticks = [candlesticks]
        Logger.WriteTradingObjectOrdered(file, candlesticks)


    @staticmethod
    def LogTrades(trades):
        file = TRADES_TRADING
        if not os.path.isfile(file):
            io.open(file, 'w', encoding='utf-8')
        Logger.WriteTradingObjectOrdered(file, trades)



#########################################################################################
#########################################################################################
#########################################################################################

#########################################################################################
####################### FUNCTIONS TO WRITE IN THE FILE ##################################
#########################################################################################

    @staticmethod
    def UpdateJsonObject(file, key, object):
        if os.path.getsize(file) == 0:
            with io.open(file, 'w', encoding='utf-8') as f:
                object = {str(key) : object.toJSON()}
                f.write(json.dumps(object, ensure_ascii=False, sort_keys=True, indent=4))
                f.write('\n')
                f.flush()
                f.close()
        else:
            with io.open(file) as f_read:
                data = dict(json.load(f_read))
                f_read.close()
            delete = (False, )
            for k,m in data.items():
                if str(m['Id']) == str(object.id):
                    delete = (True, k)
            if delete[0]:
                Logger.LogInfo('Override of previous object.' + str(type(object)) + '. Id: ' + str(object.id), 'Logger')
                del  data[delete[1]]
            data.update({key : object.toJSON()})
            with io.open(file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))
                f.write('\n')
                f.flush()
                f.close()

    @staticmethod
    def WriteTradingObject(file, tradingObject):
        if os.path.getsize(file) == 0:
            with io.open(file, 'w', encoding='utf-8') as f:
                data = {}
                for obj in tradingObject:
                    data[obj.toID()] = obj.toData()
                json.dump(data, f, indent=4)
                f.flush()
                f.close()
        else:
            with io.open(file) as f_read:
                data = dict(json.load(f_read))
                f_read.close()
                for obj in tradingObject:
                    data.update({obj.toID() : obj.toData()})
            with io.open(file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                f.flush()
                f.close()

    @staticmethod
    def WriteTradingObjectOrdered(file, tradingObject):
        if os.path.getsize(file) == 0:
            with io.open(file, 'w', encoding='utf-8') as f:
                data = []
                for obj in tradingObject:
                    data.append((obj.toID(), obj.toData()))
                json.dump(OrderedDict(data), f, sort_keys=False, indent=4)
                f.flush()
                f.close()
        else:
            with io.open(file) as f_read:
                data = json.load(f_read, object_pairs_hook=OrderedDict)
                f_read.close()
                for obj in tradingObject:
                    data.update({obj.toID(): obj.toData()})
            with io.open(file, 'w', encoding='utf-8') as f:
                json.dump(data, f, sort_keys=False, indent=4)
                f.flush()
                f.close()

    @staticmethod
    def WriteJson(file, key, dictionnary):
        if os.path.getsize(file) == 0:
            with io.open(file, 'w', encoding='utf-8') as f:
                object = {str(key) : dictionnary}
                f.write(json.dumps(object, ensure_ascii=False, sort_keys=True, indent=4))
                f.write('\n')
                f.flush()
                f.close()
        else:
            with io.open(file) as f_read:
                data = dict(json.load(f_read))
                f_read.close()
            delete = (False,)
            for k, m in data.items():
                if str(k) == str(key):
                    delete = (True, k)
            if delete[0]:
                del data[delete[1]]
            data.update({key : dictionnary})
            with io.open(file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))
                f.write('\n')
                f.flush()
                f.close()

    @staticmethod
    def Write():
        return

#########################################################################################
#########################################################################################
#########################################################################################

#########################################################################################
########################### Functions for the logging module ############################
#########################################################################################

    # For debugging directly on PyCharm replace this function with print and everything will be prompt on the IDE.
    @staticmethod
    def __log(message):
        """
        with io.open(LOGS, 'a+') as f:
            f.write(message)
            f.flush()
            f.close()"""
        print (message)

    @staticmethod
    def LogInfo(message, origin):
        output = 'INFO : ' + str(datetime.datetime.now().strftime("%H:%M:%S")) + ' ' + origin + '.py: ' + message + '\n'
        CryptoBLL.Logger.__log(output)

    @staticmethod
    def LogError(message, origin):
        output = 'ERROR : ' + str(datetime.datetime.now().strftime("%H:%M:%S")) + ' ' + origin + '.py: ' + message + '\n'
        CryptoBLL.Logger.__log(output)

    @staticmethod
    def LogWarning(message, origin):
        output = 'WARNING : ' + str(datetime.datetime.now().strftime("%H:%M:%S")) + ' ' + origin + '.py : ' + message + '\n'
        CryptoBLL.Logger.__log(output)

    @staticmethod
    def LogState(message, origin, newLines = False):
        message = 'STATE : ' + str(datetime.datetime.now().strftime("%H:%M:%S")) + ' ' + origin + '.py : ' + message + '\n'
        if (not os.path.isfile(LOGS_STATE)) or (os.path.getsize(LOGS_STATE) == 0):
            with io.open(LOGS_STATE, 'a+') as f:
                f.write(message)
                f.flush()
                f.close()
                return
        if not newLines:
            with io.open(LOGS_STATE, 'r') as f:
                lines = f.readlines()
                f.close()
            del lines[-1]
            lines.append(message)
            with io.open(LOGS_STATE, 'w') as f:
                f.writelines(lines)
                f.flush()
                f.close()
        else:
            with io.open(LOGS_STATE, 'a+') as f:
                f.write(message)
                f.flush()
                f.close()
                return
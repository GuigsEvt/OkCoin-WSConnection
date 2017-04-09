from Definition import ROOT_DIR
import datetime, urllib, os, time
#import urllib.parse as urlparse
import schedule
import CryptoBLL

class Utils(object):

    ### Get correct directory for arbitrage directory
    @staticmethod
    def getDirectoryJSONArbitrage(description='Arbitrage'):
        return (ROOT_DIR + '/JSON/' + description + '/' + description + 'Logs' + str(datetime.date.today()) + '.json')

    @staticmethod
    def convertUnixTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
        return time.mktime(time.strptime(datestr, format))

    #### Convert all values of a dict to floats
    @staticmethod
    def convert_to_floats(data):
        for key, value in data.items():
            data[key] = float(value)
        return data

    # Construct url for get method
    @staticmethod
    def constructUrl(uri, path, parameters=None):
        url = "%s/%s" % (uri, path)

        if parameters:
            keys = list(parameters.keys())
            keys.sort()
            url = "%s?%s" % (url, '&'.join(["%s=%s" % (k, parameters[k]) for k in keys]))
        return url

    # Construct url via the urlencode method
    @staticmethod
    def constructUrlBis(filters):
        if filters:
            return '?' + urlparse.urlencode(filters)
        else:
            return ''

    @staticmethod
    def InternetConnection():
        try:
            # Google adress that is one of the fastest to check network availibility
            urllib.request.urlopen('http://216.58.192.142', timeout=1)
            return True
        except urllib.request.URLError:
            return False

    # Check emptyness of a file
    @staticmethod
    def checkIfFileEmptyOrNull(file):
        if not os.path.isfile(file):
            return True
        elif (os.path.getsize(file) == 0):
            return True
        return False

    def getDirectoryJSONForAPI(exchange):
        return (ROOT_DIR + '/JSON/APIs/' + exchange + '/' + exchange + 'Logs' + str(datetime.date.today()) + '.json')

    @staticmethod
    def eventForChangingDay():
        schedule.every().day.at("17:01").do(CryptoBLL.Logger.UpdateOrderTradingFile)
        schedule.run_pending()

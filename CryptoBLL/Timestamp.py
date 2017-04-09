import time, datetime


class Timestamp(object):

    """
    Enum like object used in transaction method to specify time range
    from which to get list of transactions
    """
    DAY = 'day'
    HOUR = 'hour'
    MINUTE = 'minute'
    SECOND = 'second'

    @staticmethod
    def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
        return time.mktime(time.strptime(datestr, format))

    @staticmethod
    def getDatetimeFromTimeStamp(timestamp):
        return datetime.datetime.fromtimestamp(timestamp=timestamp).__str__()

    @staticmethod
    def post_process(self, before):
        after = before
        # Add timestamps if there isnt one but is a datetime
        if ('return' in after):
            if (isinstance(after['return'], list)):
                for x in range(0, len(after['return'])):
                    if (isinstance(after['return'][x], dict)):
                        if ('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
                            after['return'][x]['timestamp'] = float(Timestamp.createTimeStamp(after['return'][x]['datetime']))
        return after


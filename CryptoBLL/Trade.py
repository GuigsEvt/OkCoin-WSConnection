import datetime
import CryptoBLL

class Trade(object):

    # Type is either bid or ask
    # It means that the price has been executed on the bid or ask range
    def __init__(self, id, price, amount, time, type):
        self.id = id
        self.price = float(price)
        self.amount = float(amount)
        self.time = str(time)
        if type in ['bid', 'ask']:
            self.type = str(type)
        else:
            raise Exception

    def toJSON(self):
        return { 'id' : self.id,
                 'price' : self.price,
                 'amount' : self.amount,
                 'type' : self.type,
                 'time': self.time }
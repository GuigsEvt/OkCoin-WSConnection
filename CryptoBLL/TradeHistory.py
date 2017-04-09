import datetime
import CryptoBLL

class TradeHistory(object):

    # Type is either bid or ask
    # It means that the price has been executed on the bid or ask range
    def __init__(self, price, amount, time):
        self.price = float(price)
        self.amount = float(amount)
        self.time = str(time)

    def toJSON(self):
        return { 'price' : self.price,
                 'amount' : self.amount,
                 'time': self.time }
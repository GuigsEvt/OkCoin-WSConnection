from enum import Enum

class ASSETS(Enum):
    USD = 'USD'
    EURO = 'EURO'
    BITCOIN = 'BITCOIN'
    ETHEREUM = 'ETHEREUM'


Assets = {'Kraken': {ASSETS.USD: 'ZUSD',
                     ASSETS.EURO: 'ZEUR',
                     ASSETS.BITCOIN: 'XXBT',
                     ASSETS.ETHEREUM: 'XETH'},
          'Poloniex': {ASSETS.USD: 'USDT',
                       ASSETS.BITCOIN: 'BTC'},
          'Bitfinex': {ASSETS.USD: 'usd',
                       ASSETS.BITCOIN: 'btc'},
          'Itbit': {ASSETS.USD: 'USD',
                    ASSETS.BITCOIN: 'XBT',
                    ASSETS.EURO: 'EUR'}
          }

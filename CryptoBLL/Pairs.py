from enum import Enum

class PAIRS(Enum):
    BTCEUR = 1
    BTCUSD = 2
    ETHUSD = 3
    ETHBTC = 4
    ETHEUR = 5


Pairs = {'Kraken': {PAIRS.BTCEUR: 'XXBTZEUR',
                    PAIRS.ETHEUR: 'XETHZEUR',
                    PAIRS.BTCUSD: 'XXBTZUSD',
                    PAIRS.ETHUSD: 'XETHZUSD'},
         'Poloniex': {PAIRS.BTCUSD: 'USDT_BTC'},
         'Bitfinex': {PAIRS.BTCUSD: 'btcusd',
                      PAIRS.ETHUSD: 'ethusd',
                      PAIRS.ETHBTC: 'ethbtc'},
         'Itbit': {PAIRS.BTCEUR: 'XBTEUR',
                   PAIRS.BTCUSD: 'XBTUSD'},
         'Okcoin': {PAIRS.BTCUSD: 'btc_usd'}
         }

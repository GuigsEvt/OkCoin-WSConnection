OkCoin WebSocket modules to retrieve candlesticks and trades
=======================

This modules is aimed to retrieve in real time via a websocket connectio the trades and the candlesticks from the OkCoin market.

It is currently configured to get it for the BitcoinUsd pair (BTCUSD) for three differents timeframe:
- 4 hours
- 12 hours
- 24 hours

Everything is stored in a MongoDB database. Currently the connection with the mongoDB is deprecated due to changes in python version.

It should be fixed in the future but the WebSocket connection is working correctly and can be used for others purposes.

To use it with your own credentials just paste yours in InitFiles/config.ini

The following modules must be installed with pip first:

pip install requests
pip install pymongo
pip install enum
pip install configparser
pip install pymongo
pip install schedule
pip install six
pip install dateutil

Prerequisites
-------------

[MongoDb 3.4+](https://docs.mongodb.com/manual/installation/)


License
-------

The MIT License (MIT)

Copyright (c) Guigs

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

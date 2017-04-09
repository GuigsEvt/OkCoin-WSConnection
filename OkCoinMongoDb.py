#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CryptoBLL, sys
import time, pip


if not (CryptoBLL.Utils.InternetConnection()):
    CryptoBLL.Logger.LogWarning('No network connection. You cannot run the program. Check the network.', 'PFETradingCrypto')
    sys.exit()

APIsWs = CryptoBLL.APIs().getAPIsWs()

while True:
    time.sleep(10)
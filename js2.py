# -*- coding:utf-8 -*-
"""
@author: XiangNan
@desc: 
"""
import math
import time
import base64
import hashlib

timestamp = 1587102734000
print(timestamp)
token = base64.b64encode(('aiding_win' + str(timestamp)).encode())
print(token)
md = hashlib.md5(base64.b64encode(('aiding_win' + str(math.ceil(timestamp / 1000))).encode())).hexdigest()
print(md)
sign = str(math.ceil(timestamp / 1000)) + '~' + token.decode() + '|' + md
print(sign)

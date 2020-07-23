# -*- coding:utf-8 -*-
"""
@author: XiangNan
@desc: 
"""
import time
import base64
import hashlib
import requests
import pymongo
from datetime import datetime, timedelta


class JsOne:
    def __init__(self, page):
        self.page = page + 1
        self.zhao = 0
        self.token = {'value': '', 'time': datetime.now()}
        self.timestamp = None
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['js1']
        self.collection = self.db['js1_items']

    def get_token(self):
        if not (self.token and self.timestamp) or self.token['time'] < datetime.now() - timedelta(minutes=1):
            self.timestamp = str(int(time.time()))
            self.token['value'] = hashlib.md5(base64.b64encode(('9622' + self.timestamp).encode())).hexdigest()
            self.token['time'] = datetime.now()
        return self.token['value'], self.timestamp

    def request_url(self, page):
        url = f'http://www.python-spider.com/challenge/api/json?page={page}&count=14'
        safe, timestamp = self.get_token()
        headers = {
            'safe': safe,
            'timestamp': timestamp,
        }
        date = None
        try:
            response = requests.get(url, headers=headers)
            date = response.json()
        except Exception:
            print('出错了')
        return date

    def parse_response(self, date):
        info_list = []
        try:
            infos = date['infos']
            state = date['state']
            if state == "success":
                for info in infos:
                    area = info['area']
                    inputtime = datetime.strptime(info.get('inputtime', None), "%Y-%m-%d %H:%M:%S")
                    message = info.get('message', None)
                    if '招' in message:
                        self.zhao += 1
                    messagekw = info.get('messagekw', None)
                    messagetype = info.get('messagetype', None)
                    messageurl = info.get('messageurl', None)
                    pubtime = datetime.strptime(info.get('pubtime', None), "%Y-%m-%d")
                    refer = info.get('refer', None)
                    info = {
                        'area': area,
                        'inputtime': inputtime,
                        'message': message,
                        'messagekw': messagekw,
                        'messagetype': messagetype,
                        'messageurl': messageurl,
                        'pubtime': pubtime,
                        'refer': refer,
                    }
                    print('*'*50)
                    print(info)
                    print('-'*50)
                    info_list.append(info)
            else:
                print(f"解析出错了，错误-->{state}")
        except Exception as e:
            print(f"解析出错了，错误-->{e}")
        return info_list

    def save_to_mongo(self, infos):
        result = self.collection.insert_many(infos)
        return len(result.inserted_ids)

    def run(self):
        for page in range(1, self.page):
            print(f'page-->{page}')
            data = self.request_url(page)
            info_list = self.parse_response(data)
            result = self.save_to_mongo(info_list)
            print(result)


if __name__ == '__main__':
    js1 = JsOne(85)
    js1.run()
    print(js1.zhao)

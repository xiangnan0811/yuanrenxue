import math
import time
import base64
import hashlib
import requests


def get_sign():
    timestamp = int(time.time())
    token = base64.b64encode(('aiding_win' + str(timestamp)).encode())
    md = hashlib.md5(base64.b64encode(('aiding_win' + str(math.ceil(timestamp / 1000))).encode())).hexdigest()
    sign = str(math.ceil(timestamp / 1000)) + '~' + token.decode() + '|' + md
    return sign


def requests_api(page):
    url = 'http://www.python-spider.com/api/challenge6'
    # sign = get_sign()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        'Cookie': 'sign="*"'
    }

    data = {
        "page": f"{page}"
    }
    response = requests.post(url=url, headers=headers, data=data)
    return response.json()


def parse_request(response):
    value_sum = 0

    data_list = response['data']
    for data in data_list:
        value = int(data['value'].strip())
        value_sum += value
    return value_sum


def main():
    the_sum = 0
    for i in range(1, 101):
        print(f'page-->{i}')
        print(f'the_sum-->{the_sum}')
        response = requests_api(i)
        value_sum = parse_request(response)
        the_sum += value_sum
    print(the_sum)


if __name__ == "__main__":
    main()
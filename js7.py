import requests

abandon_proxy = set()


def get_proxy():
    url = 'http://127.0.0.1:5555/random'
    proxy = requests.get(url).text
    if proxy:
        return proxy
    else:
        print('获取proxy出错')
        return None


def request_api(page, retry_times=None):
    proxy = get_proxy()
    if proxy and (proxy not in abandon_proxy):
        proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
        }
        print(f'proxies--> {proxies}')
        url = 'http://www.python-spider.com/api/challenge7'
        data = {'page': page}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
        try:
            abandon_proxy.add(proxy)
            city_url = 'http://www.python-spider.com/cityjson'
            requests.post(url=city_url, headers=headers, proxies=proxies)
            response = requests.post(url=url, data=data, headers=headers, proxies=proxies, timeout=20)
            if response.ok and response.status_code == 200:
                json_data = response.json()
                if json_data['state'] == 'success':
                    return json_data
                else:
                    print('state不为success')
                    if not retry_times:
                        retry_times = 0
                    retry_times += 1
                    print(f'重试第{retry_times}次')
                    return request_api(page=page, retry_times=retry_times)
            else:
                print('没有response或状态码不是200')
                if not retry_times:
                    retry_times = 0
                retry_times += 1
                print(f'重试第{retry_times}次')
                return request_api(page=page, retry_times=retry_times)
        except Exception as e:
            print(e)
            abandon_proxy.add(proxy)
            if not retry_times:
                retry_times = 0
            retry_times += 1
            print(f'重试第{retry_times}次')
            return request_api(page=page, retry_times=retry_times)
    else:
        print('no proxy')
        abandon_proxy.add(proxy)
        if not retry_times:
            retry_times = 0
        retry_times += 1
        print(f'重试第{retry_times}次')
        return request_api(page=page, retry_times=retry_times)


def parse_response(response):
    page_total = 0
    data = response.get('data')
    for item in data:
        value = int(item.get('value'))
        print(f'value--> {value}')
        page_total += value
    return page_total


def main():
    total = 0
    for page in range(1, 101):
        print(f'page--> {page}')
        response = request_api(page)
        page_total = parse_response(response)
        total += page_total
        print(f'current total --> {total}, current page --> {page}')
    return total


if __name__ == "__main__":
    total = main()
    print(f'total--> {total}')

import requests

requests.packages.urllib3.disable_warnings()


def request_url(num):
    url = f'http://sekiro.virjar.com/invoke?group=ws-challenge-15&action=getData&num={num}'
    response = requests.get(url=url, verify=False)
    try:
        if response.status_code == 200:
            return response.json()
    except:
        return None


def parse_response(response):
    page_total = 0
    if response:
        data = response['data']
        for item in data:
            value = int(item.get('value').strip())
            print(f'value--> {value}')
            page_total += value

    return page_total


def main():
    total = 0
    for num in range(1, 101):
        print(f'page--> {num}')
        response = request_url(num)
        page_total = parse_response(response)
        total += page_total

    return total


if __name__ == "__main__":
    total = main()
    print(f'total--> {total}')

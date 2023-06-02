import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent

import datetime
#
# headers = {
#
#     'User-Agent': fake_useragent.
#
# }

def getData(city_code='2398'):

    headers = {
        'authority': 'web-gateway.middle-api.magnit.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://magnit.ru',
        'referer': 'https://magnit.ru/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-app-version': '0.1.0',
        'x-client-name': 'magnit',
        'x-device-id': 'x2h29qw60g',
        'x-device-platform': 'Web',
        'x-device-tag': 'disabled',
        'x-platform-version': 'window.navigator.userAgent',
    }

    params = {
        'offset': '0',
        'limit': '36',
        'storeId': '102053',
        'sortBy': 'priority',
        'order': 'desc',
        'adult': 'true',
    }

    response = requests.get('https://web-gateway.middle-api.magnit.ru/v1/promotions?offset=0&limit=36&storeId=102053&sortBy=priority&order=desc&adult=true', headers=headers, params=params)

    items_count = response.json().get('total')

    response = requests.get(f'https://web-gateway.middle-api.magnit.ru/v1/promotions?offset=0&limit={items_count}&storeId=102053&sortBy=priority&order=desc&adult=true', headers=headers, params=params)

    with open('data.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(

            (
                'Продукт',
                'Старая цена',
                'Новая цена',
                'Процент скидки',
                'Конец акции'
            )

        )

    for item in response.json().get('data'):

        with open('data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)

            try:
                price = item['price']
            except:
                price = '-'

            if price == '-':
                continue

            try:
                oldPrice = str(item['oldPrice'])[:-2]
            except:
                oldPrice = '-'

            try:
                discountPercentage = item['discountPercentage']
            except:
                discountPercentage = '-'



            writer.writerow(

                (
                    item['name'],
                    oldPrice,
                    str(item['price'])[:-2],
                    discountPercentage,
                    item['endDate']
                )

            )

    print('Файл успешно записан')


def main():
    getData(city_code='2398')


if __name__ == '__main__':
    main()
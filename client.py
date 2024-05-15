import requests.exceptions

from utils import get_env_variable
from methods import get_request_proxy


class KaspiClient:
    def __init__(self):
        self.host = get_env_variable('KASPI_HOST')
        self.token = get_env_variable('KASPI_SHOP_TOKEN')

        self.headers = {'Content-Type': 'application/vnd.api+json',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                        'X-Auth-Token': self.token}  # in my case shop - Sman

        self.params = None

    def get_meta_info(self, start_date: int, end_date: int):
        path = self.host + 'orders'

        self.params = {
            'page[number]': 0,
            'page[size]': 100,
            'filter[orders][state]': 'ARCHIVE',
            'filter[orders][creationDate][$ge]': start_date,
            'filter[orders][creationDate][$le]': end_date
        }

        try:
            meta = get_request_proxy(path=path, key='meta', headers=self.headers, params=self.params)
        except requests.exceptions.HTTPError as e:
            print(e)
            return list()

        return meta

    def get_orders(self, page_number: int, page_size: int, start_date: int, end_date: int):
        # dates in milliseconds

        path = self.host + 'orders'

        self.params = {
            'page[number]': page_number,
            'page[size]': page_size,
            'filter[orders][state]': 'ARCHIVE',
            'filter[orders][creationDate][$ge]': start_date,
            'filter[orders][creationDate][$le]': end_date
        }

        try:
            data = get_request_proxy(path=path, key='data', headers=self.headers, params=self.params)
        except requests.exceptions.HTTPError as e:
            print(e)
            return list()

        return data

    def get_page_cnt_of_orders(self, start_milliseconds: int, end_milliseconds: int):
        meta = self.get_meta_info(start_date=start_milliseconds, end_date=end_milliseconds)

        try:
            return meta['pageCount']
        except Exception as e:
            print('no orders between these dates')
            return 0

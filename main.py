import logging
import csv

from datetime import datetime, timedelta
from client import KaspiClient
from convert import convert_datetime_to_milliseconds as conv_d
from convert import convert_datetime_from_milliseconds as conv_d_rev

from decorators import measure_time

connector = KaspiClient()

logger = logging.getLogger(__name__)


def write_to_csv_file(data: list, file_name: str):
    with open(f'{file_name}.csv', 'a') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data)


def parse(page_number: int, start_date: int, end_date: int):
    data = connector.get_orders(page_number=page_number, page_size=100, start_date=start_date, end_date=end_date)

    for d in data:
        order = {'id': d['id'],
                 'phone_number': d['attributes']['customer']['cellPhone'],
                 'first_name': d['attributes']['customer']['firstName'],
                 'last_name': d['attributes']['customer']['lastName'],
                 'date': conv_d_rev(d['attributes']['creationDate'])}

        write_to_csv_file([order['id'], order['first_name'], order['last_name'], order['phone_number'], order['date']],
                          file_name=file_name)


@measure_time
def func(start_d: str, end_d: str, file_name: str):
    start_date = datetime.strptime(start_d, '%Y-%m-%d')
    end_date = datetime.strptime(end_d, '%Y-%m-%d')

    write_to_csv_file(data=['Номер заказа', 'Телефон', 'Имя клиента', 'Фамилия клиента', 'Дата заказа'],
                      file_name=file_name)

    while start_date < end_date:
        next_date = start_date + timedelta(days=14)

        # calc
        page_cnt = connector.get_page_cnt_of_orders(start_milliseconds=conv_d(start_date),
                                                    end_milliseconds=conv_d(next_date))

        print('parsing dates between: %s and %s. pageCnt = %s' % (start_date, next_date, page_cnt))

        for page in range(page_cnt + 1):
            parse(page_number=page, start_date=conv_d(start_date), end_date=conv_d(next_date))

        start_date = next_date


if __name__ == '__main__':
    start_d = input('Start date in format %Y-%M-%D: ')
    end_d = input('End date in format %Y-%M-%D: ')

    file_name = input('Output file name: ')

    func(start_d=start_d, end_d=end_d, file_name=file_name)
